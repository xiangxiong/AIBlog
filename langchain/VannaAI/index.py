"""
最小可运行的 Vanna AI Demo:
1) 创建本地 SQLite 示例数据库
2) 使用 Vanna 2.x 的 OpenAI 兼容 LLM 服务接入 DeepSeek
3) 根据自然语言问题生成 SQLite SQL 并执行（支持交互式提问）

推荐在同目录创建 .env:
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
VANNA_MODEL=deepseek-chat

或使用 OpenAI:
OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=https://api.openai.com/v1
VANNA_MODEL=gpt-4o-mini
"""

from __future__ import annotations

import asyncio
import os
import re
import sqlite3
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from vanna import User
from vanna.core.llm import LlmMessage, LlmRequest
from vanna.integrations.openai import OpenAILlmService


SYSTEM_PROMPT = """
你是一个专业的数据分析助手，负责把用户的中文问题转换成 SQLite SQL。

数据库只有一张表:

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city TEXT NOT NULL,
    amount REAL NOT NULL,
    order_date TEXT NOT NULL
);

业务含义:
- orders 是订单表
- amount 是订单金额
- city 是城市
- order_date 是订单日期，格式为 YYYY-MM-DD

要求:
- 只返回一条可执行的 SQLite SELECT SQL
- 不要返回 Markdown
- 不要解释
- 不要生成 INSERT、UPDATE、DELETE、DROP、ALTER 等写操作
""".strip()


def build_vanna_config() -> dict:
    """
    构建 LLM 配置（OpenAI 兼容接口）。
    优先使用 DeepSeek 环境变量；否则回落到 OpenAI。
    """
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    api_key = deepseek_key or openai_key

    if not api_key:
        raise RuntimeError(
            "未检测到 API Key。请在 .env 或环境变量中设置 DEEPSEEK_API_KEY 或 OPENAI_API_KEY。"
        )

    using_deepseek = bool(deepseek_key)
    default_base_url = (
        "https://api.deepseek.com/v1"
        if using_deepseek
        else "https://api.openai.com/v1"
    )
    default_model = "deepseek-chat" if using_deepseek else "gpt-4o-mini"

    base_url = (
        os.getenv("DEEPSEEK_BASE_URL")
        if using_deepseek
        else os.getenv("OPENAI_BASE_URL")
    )
    model = os.getenv("VANNA_MODEL", default_model)

    config = {
        "api_key": api_key,
        "model": model,
        "base_url": base_url or default_base_url,
    }
    return config


def bootstrap_demo_db(db_path: Path) -> None:
    """初始化一个非常小的订单表数据，便于演示 NL2SQL。"""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            city TEXT NOT NULL,
            amount REAL NOT NULL,
            order_date TEXT NOT NULL
        );
        """
    )

    cursor.execute("DELETE FROM orders;")
    cursor.executemany(
        """
        INSERT INTO orders (id, customer_name, city, amount, order_date)
        VALUES (?, ?, ?, ?, ?);
        """,
        [
            (1, "Alice", "Shanghai", 199.0, "2026-05-01"),
            (2, "Bob", "Beijing", 299.0, "2026-05-01"),
            (3, "Cindy", "Shanghai", 149.0, "2026-05-02"),
            (4, "David", "Shenzhen", 399.0, "2026-05-02"),
            (5, "Eva", "Beijing", 259.0, "2026-05-03"),
        ],
    )

    conn.commit()
    conn.close()


def clean_sql(sql: str) -> str:
    """兼容模型偶尔返回 Markdown 代码块的情况。"""
    sql = sql.strip()
    sql = re.sub(r"^```(?:sql)?", "", sql, flags=re.IGNORECASE).strip()
    sql = re.sub(r"```$", "", sql).strip()
    return sql


def run_sql(db_path: Path, sql: str) -> pd.DataFrame:
    normalized_sql = sql.strip().lower()
    if not normalized_sql.startswith(("select", "with")):
        raise ValueError(f"为了安全，demo 只允许执行 SELECT/WITH 查询。当前 SQL: {sql}")

    conn = sqlite3.connect(db_path)
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()


async def generate_sql(
    llm: OpenAILlmService,
    question: str,
    temperature: float = 0.1,
) -> str:
    user = User(id="demo-user", username="demo")
    request = LlmRequest(
        user=user,
        system_prompt=SYSTEM_PROMPT,
        messages=[LlmMessage(role="user", content=question)],
        stream=False,
        temperature=temperature,
    )
    response = await llm.send_request(request)

    if not response.content:
        raise RuntimeError("模型没有返回 SQL，请重试或换一个问题。")

    return clean_sql(response.content)


async def run_question(llm: OpenAILlmService, db_path: Path, question: str) -> None:
    generated_sql = await generate_sql(llm=llm, question=question)

    print("\n=== Question ===")
    print(question)
    print("\n=== Generated SQL ===")
    print(generated_sql)

    result_df = run_sql(db_path=db_path, sql=generated_sql)
    print("\n=== Query Result ===")
    print(result_df)


async def main() -> None:
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

    root_dir = Path(__file__).resolve().parent
    db_path = root_dir / "demo.sqlite"
    bootstrap_demo_db(db_path)

    config = build_vanna_config()
    llm = OpenAILlmService(
        api_key=config["api_key"],
        base_url=config["base_url"],
        model=config["model"],
    )

    print("\n=== Vanna Demo Ready ===")
    print(f"model: {config['model']}")
    print(f"base_url: {config['base_url']}")
    print("输入自然语言问题开始查询，输入 q 退出。\n")

    # 先跑一条默认问题，便于快速验证
    await run_question(llm, db_path, "每个城市的销售总额是多少？按总额从高到低排序")

    while True:
        question = input("\n请输入问题> ").strip()
        if question.lower() in {"q", "quit", "exit"}:
            print("已退出。")
            break
        if not question:
            continue
        await run_question(llm, db_path, question)


if __name__ == "__main__":
    asyncio.run(main())

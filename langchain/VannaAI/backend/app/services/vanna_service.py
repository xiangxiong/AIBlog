from __future__ import annotations
import json
import re
from vanna import User
from vanna.core.llm import LlmMessage, LlmRequest
from vanna.integrations.openai import OpenAILlmService
from app.models import QueryResult


class VannaService:
    def __init__(self, llm_config: dict[str, str]) -> None:
        self.llm = OpenAILlmService(
            api_key=llm_config["api_key"],
            base_url=llm_config["base_url"],
            model=llm_config["model"],
        )

    async def generate_sql(self, question: str, schema_context: str) -> str:
        request = LlmRequest(
            user=User(id="vanna-demo-user", username="demo"),
            system_prompt=self._build_system_prompt(schema_context),
            messages=[LlmMessage(role="user", content=question)],
            stream=False,
            temperature=0.1,
        )
        response = await self.llm.send_request(request)
        if not response.content:
            raise RuntimeError("模型没有返回 SQL。")
        return self._clean_sql(response.content)

    async def summarize(self, question: str, sql: str, result: QueryResult) -> str:
        preview = {
            "columns": result.columns,
            "rows": result.rows[:20],
            "row_count": result.row_count,
        }
        request = LlmRequest(
            user=User(id="vanna-demo-user", username="demo"),
            system_prompt="你是数据分析助手。请基于用户问题、SQL 和查询结果，用中文给出简洁业务解读，不要编造结果中不存在的数据。",
            messages=[
                LlmMessage(
                    role="user",
                    content=(
                        f"问题: {question}\n\n"
                        f"SQL: {sql}\n\n"
                        f"查询结果 JSON: {json.dumps(preview, ensure_ascii=False)}"
                    ),
                )
            ],
            stream=False,
            temperature=0.2,
        )
        response = await self.llm.send_request(request)
        return response.content.strip() if response.content else ""

    def _build_system_prompt(self, schema_context: str) -> str:
        return f"""
你是一个专业的数据分析助手，负责把用户的中文问题转换成 PostgreSQL SQL。

{schema_context}

要求:
- 只返回一条可执行的 PostgreSQL SELECT SQL。
- 不要返回 Markdown。
- 不要解释。
- 不要生成 INSERT、UPDATE、DELETE、DROP、ALTER、TRUNCATE、CREATE 等写操作。
- 不要查询 chat_sessions、chat_messages、query_logs 这些应用内部表。
- 日期聚合可使用 DATE_TRUNC。
- 当涉及订单金额、利润、退款率时，优先使用上面的常用指标定义。
""".strip()

    def _clean_sql(self, sql: str) -> str:
        sql = sql.strip()
        sql = re.sub(r"^```(?:sql)?", "", sql, flags=re.IGNORECASE).strip()
        sql = re.sub(r"```$", "", sql).strip()
        return sql

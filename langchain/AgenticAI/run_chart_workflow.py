#!/usr/bin/env python3
"""
Agentic AI M2 — 图表生成反思 Workflow（独立脚本版）

用法:
    cd langchain/AgenticAI
    python run_chart_workflow.py

    python run_chart_workflow.py --instruction "对比2024和2025年Q1各咖啡品类销售额"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import utils

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INSTRUCTION = (
    "Create a plot comparing Q1 coffee sales in 2024 and 2025 "
    "using the data in coffee_sales.csv."
)


def generate_chart_code(instruction: str, model: str, out_path_v1: str) -> str:
    prompt = f"""
    You are a data visualization expert.

    Return your answer *strictly* in this format:

    <execute_python>
    # valid python code here
    </execute_python>

    Do not add explanations, only the tags and the code.

    The code should create a visualization from a DataFrame 'df' with these columns:
    - date   (datetime64 — already parsed; use df['date'].dt.year, df['date'].dt.month, etc.)
    - time   (string, HH:MM — do NOT concatenate or combine with the date column)
    - cash_type (string: 'card' or 'cash')
    - card (string)
    - price (number)
    - coffee_name (string)
    - quarter (int, 1–4 — already computed, use directly)
    - month  (int, 1–12 — already computed, use directly)
    - year   (int, e.g. 2024 — already computed, use directly)

    User instruction: {instruction}

    Requirements for the code:
    1. Assume the DataFrame is already loaded as 'df'.
    2. Use matplotlib for plotting.
    3. Add clear title, axis labels, and legend if needed.
    4. Save the figure as '{out_path_v1}' with dpi=300.
    5. Do not call plt.show().
    6. Close all plots with plt.close().
    7. Add all necessary import python statements
    8. CRITICAL: 'date' is datetime64 — never use string concatenation on it.
       Filter by year/quarter using the 'year' and 'quarter' integer columns.

    Return ONLY the code wrapped in <execute_python> tags.
    """
    return utils.get_response(model, prompt)


def reflect_on_image_and_regenerate(
    chart_path: str,
    instruction: str,
    model_name: str,
    out_path_v2: str,
    code_v1: str,
) -> tuple[str, str]:
    media_type, b64 = utils.encode_image_b64(chart_path)

    prompt = f"""
    You are a data visualization expert.
    Your task: critique the attached chart and the original code against the given instruction,
    then return improved matplotlib code.

    Original code (for context):
    {code_v1}

    OUTPUT FORMAT (STRICT):
    1) First line: a valid JSON object with ONLY the "feedback" field.
    Example: {{"feedback": "The legend is unclear and the axis labels overlap."}}

    2) After a newline, output ONLY the refined Python code wrapped in:
    <execute_python>
    ...
    </execute_python>

    3) Import all necessary libraries in the code. Don't assume any imports from the original code.

    HARD CONSTRAINTS:
    - Do NOT include Markdown, backticks, or any extra prose outside the two parts above.
    - Use pandas/matplotlib only (no seaborn).
    - Assume df already exists; do not read from files.
    - Save to '{out_path_v2}' with dpi=300.
    - Always call plt.close() at the end (no plt.show()).
    - Include all necessary import statements.

    IMPORTANT: The 'date' column is already a pandas datetime64 type.
    - Do NOT concatenate 'date' with 'time' using string operations.
    - To filter by year/quarter, use: df[df['year'] == 2024] or df['date'].dt.year == 2024
    - The 'quarter' and 'year' columns already exist as integers; use them directly.

    Instruction:
    {instruction}
    """

    content = utils.image_openai_call(model_name, prompt, media_type, b64)

    lines = content.strip().splitlines()
    json_line = lines[0].strip() if lines else ""

    try:
        obj = json.loads(json_line)
    except json.JSONDecodeError:
        m_json = re.search(r"\{.*?\}", content, flags=re.DOTALL)
        if m_json:
            try:
                obj = json.loads(m_json.group(0))
            except json.JSONDecodeError as e:
                obj = {"feedback": f"Failed to parse JSON: {e}"}
        else:
            obj = {"feedback": "Failed to find JSON in model response"}

    m_code = re.search(r"<execute_python>([\s\S]*?)</execute_python>", content)
    refined_code_body = m_code.group(1).strip() if m_code else ""
    refined_code = utils.ensure_execute_python_tags(refined_code_body)
    feedback = str(obj.get("feedback", "")).strip()
    return feedback, refined_code


def extract_and_exec(code_with_tags: str, df) -> None:
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", code_with_tags)
    if not match:
        raise RuntimeError("未找到 <execute_python> 代码块")
    exec(match.group(1).strip(), {"df": df})


def log_section(title: str) -> None:
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


def run_workflow(
    dataset_path: str,
    user_instructions: str,
    generation_model: str,
    reflection_model: str,
    image_basename: str = "chart",
) -> dict:
    dataset_path = str(Path(dataset_path).resolve())
    out_v1 = str(SCRIPT_DIR / f"{image_basename}_v1.png")
    out_v2 = str(SCRIPT_DIR / f"{image_basename}_v2.png")

    log_section("Step 0: 加载数据")
    df = utils.load_and_prepare_data(dataset_path)
    print(df.sample(n=3).to_string(index=False))

    log_section("Step 1: 生成 V1 代码")
    code_v1 = generate_chart_code(user_instructions, generation_model, out_v1)
    print(code_v1)

    log_section("Step 2: 执行 V1")
    extract_and_exec(code_v1, df)
    print(f"已保存: {out_v1}")

    log_section("Step 3: 反思并生成 V2 代码")
    feedback, code_v2 = reflect_on_image_and_regenerate(
        chart_path=out_v1,
        instruction=user_instructions,
        model_name=reflection_model,
        out_path_v2=out_v2,
        code_v1=code_v1,
    )
    print(f"Feedback: {feedback}\n")
    print(code_v2)

    log_section("Step 4: 执行 V2")
    extract_and_exec(code_v2, df)
    print(f"已保存: {out_v2}")

    return {
        "code_v1": code_v1,
        "chart_v1": out_v1,
        "feedback": feedback,
        "code_v2": code_v2,
        "chart_v2": out_v2,
    }

def main() -> int:
    os.chdir(SCRIPT_DIR)

    parser = argparse.ArgumentParser(description="Agentic 图表反思 Workflow")
    parser.add_argument(
        "--dataset",
        default="coffee_sales.csv",
        help="CSV 数据路径（默认 coffee_sales.csv）",
    )
    parser.add_argument(
        "--instruction",
        default=DEFAULT_INSTRUCTION,
        help="图表需求（自然语言）",
    )
    parser.add_argument(
        "--generation-model",
        default=os.getenv("GLM_GENERATION_MODEL", "glm-4-flash"),
        help="代码生成模型",
    )
    parser.add_argument(
        "--reflection-model",
        default=os.getenv("GLM_REFLECTION_MODEL", "glm-4v-plus"),
        help="看图反思模型",
    )
    parser.add_argument(
        "--basename",
        default="chart",
        help="输出图片文件名前缀",
    )
    args = parser.parse_args()

    try:
        result = run_workflow(
            dataset_path=args.dataset,
            user_instructions=args.instruction,
            generation_model=args.generation_model,
            reflection_model=args.reflection_model,
            image_basename=args.basename,
        )
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        return 1

    log_section("完成")
    print(f"V1: {result['chart_v1']}")
    print(f"V2: {result['chart_v2']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

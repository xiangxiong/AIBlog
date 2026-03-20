import os
import re
import json
import time

import langchain
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser



# 业务场景：电商客户反馈处理系统
# 需求描述
# 某电商平台需要自动处理客户反馈，实现以下功能：
#
# 情感分析：判断用户反馈的情感倾向
#
# 问题分类：识别反馈中的问题类型
#
# 紧急程度评估：根据内容判断处理优先级
#
# 生成回复草稿：根据分析结果生成初步回复



# 使用通义千问模型
qwen = ChatTongyi(
    model_name="qwen-max",
    temperature=0.2,  # 控制创造性
    max_tokens=2000,  # 最大输出长度
    streaming=False,  # 关闭流式输出
    enable_search=True  # 启用联网搜索增强
)


# 辅助函数：带重试的模型调用  LLM
def call_qwen_with_retry(prompt, max_retries=3, retry_delay=2):
    """带错误重试的千问模型调用"""
    for attempt in range(max_retries):
        try:
            response = qwen.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"模型调用失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
            time.sleep(retry_delay)
    return "模型服务暂时不可用，请稍后再试。"


# 业务处理函数（使用千问模型）----------------
# 提取订单ID  ERP 订单系统
def extract_order_id(text: str) -> dict:
    """使用千问模型提取订单ID"""
    prompt = f"""
    你是一个电商订单处理专家，请从以下客户反馈中提取订单ID：
    {text}

    订单ID通常是"ORD"开头的10位数字组合。如果找不到订单ID，返回"NOT_FOUND"。

    请严格按JSON格式返回结果：{{"order_id": "提取结果"}}
    """

    try:
        # 正则提取
        match = re.search(r'ORD\d{10}', text)
        return {"order_id": match.group(0) if match else "NOT_FOUND"}
    except:
        # 备选方案：大模型提取
        result = call_qwen_with_retry(prompt)
        # 尝试解析JSON
        return json.loads(result.strip())

# 情感分类
def analyze_sentiment(text: str) -> dict:
    """使用千问模型进行情感分析"""
    prompt = f"""
    请分析以下客户反馈的情感倾向：
    「{text}」

    要求：
    1. 判断情感类型：POSITIVE(积极)/NEUTRAL(中性)/NEGATIVE(消极)
    2. 评估置信度(0.0-1.0)
    3. 提取3个关键短语

    返回JSON格式：
    {{
        "sentiment": "情感类型",
        "confidence": 置信度,
        "key_phrases": ["短语1", "短语2", "短语3"]
    }}
    """

    try:
        # 调用千问模型
        result = call_qwen_with_retry(prompt)
        output_parser = JsonOutputParser()
        result = output_parser.parse(result)
        return result
    except Exception as e:
        print(f"情感分析失败: {e}")
        return {
            "sentiment": "NEUTRAL",
            "confidence": 0.7,
            "key_phrases": []
        }

# 问题分类
def classify_issue(text: str) -> dict:
    """使用千问模型进行问题分类"""
    prompt = f"""
    作为电商客服专家，请对以下客户反馈进行分类：
    「{text}」

    分类选项：
    - 物流问题：配送延迟、物流损坏等
    - 产品质量：商品瑕疵、功能故障等
    - 客户服务：客服态度、响应速度等
    - 支付问题：扣款异常、退款延迟等
    - 退货退款：退货流程、退款金额等
    - 其他：无法归类的反馈

    要求：
    1. 选择最相关的1-2个分类
    2. 按相关性排序

    返回JSON格式：{{"categories": ["分类1", "分类2"]}}
    """

    try:
        #  调用千问模型
        result = call_qwen_with_retry(prompt)
        output_parser = JsonOutputParser()
        result = output_parser.parse(result)
        return result
    except Exception as e:
        print(f"问题分类失败: {e}")
        return {"categories": ["其他"]}

# 紧急状态评估
def assess_urgency(text: str) -> dict:
    """使用千问模型评估紧急程度"""
    prompt = f"""
    作为客服主管，请评估以下客户反馈的紧急程度：
    「{text}」

    评估标准：
    - HIGH(高)：包含"紧急"、"立刻"、"马上"或威胁投诉
    - MEDIUM(中)：表达强烈不满但无立即行动要求
    - LOW(低)：一般反馈或建议

    返回JSON格式：
    {{
        "urgency": "紧急级别",
        "sla_hours": 响应时限(小时),
        "reason": "评估理由"
    }}
    """

    try:
        result = call_qwen_with_retry(prompt)
        output_parser = JsonOutputParser()
        result = output_parser.parse(result)
        # 确保数值类型
        result["sla_hours"] = int(result["sla_hours"])
        return result
    except Exception as e:
        print(f"紧急度评估失败: {e}")
        return {
            "urgency": "MEDIUM",
            "sla_hours": 24,
            "reason": "评估失败"
        }


def generate_response(data: dict) -> dict:
    print(data)
    """使用千问模型生成定制化回复"""
    prompt_template = """
    你是一名资深电商客服专家，请根据以下分析结果生成客户回复：

    ### 客户反馈原文：
    {feedback}

    ### 分析结果：
    - 订单ID：{order_id}
    - 情感倾向：{sentiment} (置信度：{confidence:.2f})
    - 问题类型：{categories}
    - 紧急程度：{urgency} (需在{sla_hours}小时内响应)
    {key_phrases_section}

    ### 回复要求：
    1. 根据情感倾向调整语气：
       - 积极反馈：表达感谢，适当赞美
       - 消极反馈：诚恳道歉，明确解决方案
    2. 包含订单ID和问题分类
    3. 明确说明处理时限和后续步骤
    4. 长度100-150字，使用自然口语
    5. 结尾询问是否还有其他问题

    请直接输出回复内容，不需要额外说明。
    """

    # 构建关键短语部分
    key_phrases = data.get("key_phrases", [])
    if key_phrases:
        key_phrases_section = "- 关键要点：" + "，".join(key_phrases[:3])
    else:
        key_phrases_section = ""

    # 填充模板
    prompt = prompt_template.format(
        feedback=data["original_feedback"],
        order_id=data["order_id"],
        sentiment=data["sentiment"],
        confidence=data.get("confidence", 0.8),
        categories="、".join(data["categories"]),
        urgency=data["urgency"],
        sla_hours=data["sla_hours"],
        key_phrases_section=key_phrases_section
    )

    try:
        response = call_qwen_with_retry(prompt)

        # 添加紧急标识
        if data["urgency"] == "HIGH":
            response = f"[紧急] {response}"

        return {
            "final_response": response,
            "assigned_team": data["categories"][0] if data["categories"] else "General",
            "result":data
        }

    except Exception as e:
        print(f"回复生成失败: {e}")
        return {
            "final_response": "感谢您的反馈，我们的团队将尽快处理您的问题。",
            "assigned_team": "General"
        }


# 构建LCEL处理链 --------------------------------

# 步骤1: 基础信息提取
"""
返回的数据格式：
{
  "order_id": {
    "order_id": "ORD2024071501"  # 或 "NOT_FOUND"
  },
  "original_feedback": "原始反馈文本"
}
"""
# lambda 表达式，简化形式，匿名函数的定义
# def fun(x):
#     return x

extract_chain = RunnableParallel(
    order_id=RunnableLambda(extract_order_id),
    original_feedback=lambda x: x
)

# 步骤2: 并行分析任务
# 参数：用户对应的反馈
"""
返回的数据格式：
{
  "sentiment": {
    "sentiment": "NEGATIVE",  # 情感类型
    "confidence": 0.92,       # 置信度
    "key_phrases": ["物流太慢", "承诺三天", "实际七天"]  # 关键短语
  },
  "categories": {
    "categories": ["物流问题"]  # 问题分类
  },
  "urgency": {
    "urgency": "HIGH",        # 紧急程度
    "sla_hours": 4,           # 响应时限(小时)
    "reason": "包含紧急处理要求"  # 评估理由
  }
}
"""
# 节省大模型处理的时间，使用并行处理
analysis_chain = RunnableParallel(
# 情感分析
    sentiment=RunnableLambda(analyze_sentiment),
# 问题分类
    categories=RunnableLambda(classify_issue),
# 紧急程度
    urgency=RunnableLambda(assess_urgency)
)
# 步骤3: 组合完整流程
processing_chain = (
        # 订单提取，正则表达式，异常才会用大模型
        extract_chain
        |
        # 根据输入问题分类，情感分类，紧急程度
        RunnablePassthrough.assign(
            analysis=lambda x: analysis_chain.invoke(x["original_feedback"])
        )
        | {
            "original_feedback": lambda x: x["original_feedback"],
            "order_id": lambda x: x["order_id"]["order_id"],
            "sentiment": lambda x: x["analysis"]["sentiment"].get("sentiment", "NEUTRAL"),
            "confidence": lambda x: x["analysis"]["sentiment"].get("confidence", 0.8),
            "key_phrases": lambda x: x["analysis"]["sentiment"].get("key_phrases", []),
            "categories": lambda x: x["analysis"]["categories"]["categories"],
            "urgency": lambda x: x["analysis"]["urgency"]["urgency"],
            "sla_hours": lambda x: x["analysis"]["urgency"]["sla_hours"],
            "urgency_reason": lambda x: x["analysis"]["urgency"].get("reason", "")
        }
        # 生成答案
        | RunnableLambda(generate_response)
)



# 部署为API服务
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
app = FastAPI(title="电商客服系统")


class FeedbackRequest(BaseModel):
    content: str
    user_id: str = "anonymous"

@app.get("/")
async def read_index():
    return FileResponse("index.html")

# async  awaite一起使用，前端js是类似的用法，并行获取数据
@app.post("/process-feedback")
async def process_feedback(request: FeedbackRequest):
    try:
        start = time.time()
        result = processing_chain.invoke(request.content)
        elapsed = time.time() - start

        return {
            "success": True,
            "processing_time": f"{elapsed:.2f}s",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理失败: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


# 本地测试运行 --------------------------------
# if __name__ == "__main__":
#     # 真实客户反馈案例
#     feedback_samples = [
#         "订单ORD2024071501的物流太慢了，承诺三天实际七天才到！紧急处理！",
#         # "产品质量很好，但客服态度差劲，要求退货",
#         # "支付系统扣款异常，多扣了200元，立刻解决！否则我将投诉至消费者协会",
#         # "非常喜欢新买的耳机，音质优秀，配送也快",
#         # "订单ORD2024071502的商品与描述严重不符，虚假宣传！要求赔偿！"
#     ]
#
#     for i, feedback in enumerate(feedback_samples, 1):
#         print(f"\n{'=' * 50}\n案例 #{i}: {feedback}")
#
#         start_time = time.time()
#
#         try:
#             result = processing_chain.invoke(feedback)
#
#             elapsed = time.time() - start_time
#             print(f"[处理耗时: {elapsed:.2f}秒]")
#             data = result["result"]
#             print("\n分析结果:")
#             print(f"- 订单ID: {data.get('order_id', 'N/A')}")
#             print(f"- 情感: {data.get('sentiment', 'N/A')}")
#             print(f"- 问题类型: {', '.join(data.get('categories', []))}")
#             print(f"- 紧急度: {data.get('urgency', 'N/A')}")
#             print(f"- 分配团队: {result.get('assigned_team', 'N/A')}")
#             print(f"\n生成回复:\n{result.get('final_response', '')}")
#             print("\n" + "-" * 50)
#
#         except Exception as e:
#             print(f"处理失败: {str(e)}")
#             continue


# 生产环境增强功能 感兴趣的可以了解--------------------------------

# 1. 批量处理优化
# def batch_process_feedbacks(feedbacks, batch_size=5):
#     """批量处理客户反馈"""
#     from langchain_core.runnables import RunnableMap
#
#     batch_chain = RunnableMap({
#         "results": lambda x: [processing_chain.invoke(fb) for fb in x]
#     })
#
#     results = []
#     for i in range(0, len(feedbacks), batch_size):
#         batch = feedbacks[i:i + batch_size]
#         results.extend(batch_chain.invoke(batch)["results"])
#         print(f"已处理 {min(i + batch_size, len(feedbacks))}/{len(feedbacks)} 条反馈")
#         time.sleep(1)  # 避免速率限制
#
#     return results
#
#
# # 2. 监控与日志
# import logging
# from datetime import datetime
#
# # 配置日志
# logging.basicConfig(filename='customer_service.log',
#                     level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')
#
#
# def monitored_processing(feedback):
#     """带监控的反馈处理"""
#     start = time.time()
#     try:
#         result = processing_chain.invoke(feedback)
#         elapsed = time.time() - start
#
#         # 记录成功日志
#         logging.info(
#             f"处理成功 | 时长: {elapsed:.2f}s | 情感: {result.get('sentiment')} | 紧急度: {result.get('urgency')}")
#
#         return result
#     except Exception as e:
#         elapsed = time.time() - start
#         # 记录错误日志
#         logging.error(f"处理失败 | 时长: {elapsed:.2f}s | 错误: {str(e)}")
#         return {
#             "final_response": "系统处理遇到问题，已转人工客服处理",
#             "assigned_team": "Manual"
#         }
#
#
# # 3. 千问模型优化配置
# def optimized_qwen_call(prompt, max_tokens=1500):
#     """针对不同任务的优化调用"""
#     # 根据任务类型调整参数
#     task_type = "unknown"
#     if "情感分析" in prompt:
#         task_type = "sentiment"
#         config = {"temperature": 0.2, "max_tokens": 800}
#     elif "问题分类" in prompt:
#         task_type = "classification"
#         config = {"temperature": 0.1, "max_tokens": 600}
#     elif "紧急程度" in prompt:
#         task_type = "urgency"
#         config = {"temperature": 0.3, "max_tokens": 700}
#     else:  # 回复生成
#         task_type = "response"
#         config = {"temperature": 0.5, "max_tokens": max_tokens}
#
#     try:
#         response = qwen.invoke(prompt, **config)
#         return response.content
#     except Exception as e:
#         print(f"优化调用失败 ({task_type}): {str(e)}")
#         # 降级使用默认调用
#         return call_qwen_with_retry(prompt)
#
#
# # 4. 缓存机制
# from langchain.cache import SQLiteCache
# import langchain
#
# langchain.llm_cache = SQLiteCache(database_path=".qwen_cache.db")
#

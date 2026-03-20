from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from models import *

# Middleware 中间件
# 添加中间件的方式：在create_agent
'''
agent = create_agent(
    model=qwen_model,
    tools=[],
    middleware=[SummarizationMiddleware(), HumanInTheLoopMiddleware()],
)
'''

# 内置中间件
#   LangChain 为常见用例提供预构建的中间件：

# SummarizationMiddleware : 总结摘要的中间件
#       当接近会话次数上限时，自动汇总对话历史记录。
#  非常适合：
#     - 持续时间过长的对话超出了上下文窗口。
#     - 多轮对话，历史悠久
#     - 在需要保留完整对话上下文的应用中
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

llm = ChatOpenAI(
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    openai_api_key=os.getenv("DASHSCOPE_API_KEY"),
    model_name="qwen-max"
)
# 创建短期记忆实例
memory = InMemorySaver()
agent = create_agent(
    model=llm,
    tools=[],
    checkpointer=memory,
    # 中间件列表，可以多个，多个顺序执行
    middleware=[
        SummarizationMiddleware(
            model=llm,
            max_tokens_before_summary=80,  # 80个token 会触发 摘要总结
            messages_to_keep=1,  # 在总结后保留最后1条消息
            # 可选 summary_prompt=" 可以自定义进行摘要的提示词...",
            summary_prompt="请将以下对话历史进行简洁的摘要，保留关键信息: {messages}"
        ),
    ],
    # 打印Agent执行的过程日志
    debug= True
)

# 单一条件:当tokens> = 4000且消息> = 10时触发
# agent = create_agent(
#     model=llm,
#     tools=[weather_tool, add_tool],
#     middleware=[
#         SummarizationMiddleware(
#             model=llm_other,
#             trigger={"tokens": 4000, "messages": 10},
#             keep={"messages": 20},
#         ),
#     ],
# )
#
# # 多重条件-（任意条件必须满足 - 逻辑“或”）。
# agent2 = create_agent(
#     model="gpt-4o",
#     tools=[weather_tool, add_tool],
#     middleware=[
#         SummarizationMiddleware(
#             model="gpt-4o-mini",
#             trigger=[
#                 {"tokens": 5000, "messages": 3},
#                 {"tokens": 3000, "messages": 6},
#             ],
#             keep={"messages": 20},
#         ),
#     ],
# )

# 模拟长对话触发摘要
print("\n模拟长对话场景...")
demo_messages = [
    "用户询问你是谁",
    "用户计算商品价格：数量10，单价25.5",
    "用户再次询问你能做什么？",
    "用户想要生成一个介绍湖南的文案，要求100字左右，包含三湘四水，人文历史",
    "用户继续询问更多GPU产品信息",
    "用户要求计算2*20"
]

for i, message in enumerate(demo_messages, 1):
    print(f"\n💬 第{i}轮对话: {message}")
    # 循环调用Agent，模拟多轮对话
    result = agent.invoke({
        "messages": [HumanMessage(content=message)]},
        config={"configurable": {"thread_id": "testsummarizationMiddleware"}}
    )
    # print("执行结果："+result)


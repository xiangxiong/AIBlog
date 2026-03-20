import os
import re

# 验证模型连接
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage

llm = ChatTongyi(api_key=os.environ.get("DASHSCOPE_API_KEY"))


# 构建一个基于arxiv工具的论文查询智能体，实现根据论文编号查询论文信息的功能。
# 使用load_tools()方法导入arxiv工具：class ArxivQueryRun(BaseTool)
from langchain_community.agent_toolkits.load_tools import load_tools

# 导入arxiv工具
tools = load_tools(["arxiv"])

# 短期记忆构建：使用InMemorySaver()实现单会话的短期记忆
from langgraph.checkpoint.memory import InMemorySaver
# 创建短期记忆实例
memory = InMemorySaver()
# 系统提示词设计：简洁明了地定义Agent的角色和行为准则
system_prompt = "你是一个专业的论文查询助手，使用arxiv工具为用户查询论文信息，回答需简洁准确，包含论文标题、作者、发表时间和核心摘要。"
# 组装并调用Agent
# 使用create_agent()方法组装Agent，并通过invoke()方法调用。
from langchain.agents import create_agent

# 组装Agent
agent = create_agent(
    model=llm,
    tools=tools, #添加工具列表，绑定的论文查询的工具
    system_prompt=system_prompt,
    checkpointer=memory  # 传入记忆组件
)

# 调用Agent查询论文
result = agent.invoke(
    {"messages": [{"role": "user", "content": "请查询arxiv论文编号1605.08386的信息"}]},
    # 配置会话标识，用于区分不同用户
    config={"configurable": {"thread_id": "user_1"}}  # 会话唯一标识，用于区分不同用户
)

# 输出结果（取最后一条消息的内容）
print(result["messages"][-1].content)
"""
执行上述代码后，Agent会自动完成以下流程：

接收用户查询，识别需要调用arxiv工具
生成工具调用请求，传入论文编号1605.08386
执行arxiv工具，获取论文信息（标题、作者、发表时间、摘要）
整合工具返回结果，生成自然语言回复
"""
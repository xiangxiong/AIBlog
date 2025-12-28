import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from knowledge_base import init_retriever

# 1. 定义快递查询工具 (对应导图：快递查询API插件)
@tool
def query_express_track(tracking_number: str) -> str:
    """
    当用户询问快递进度或提供快递单号时使用。
    """
    # 模拟对接快递鸟等三方平台 [cite: 30, 50]
    return f"📦 快递单号 {tracking_number} 最新轨迹：包裹已离开上海分拨中心，正发往您的收货地址，预计明天送达！"

# 2. 定义知识库检索工具 (对应导图：使用知识库完成RAG)
def create_knowledge_tool(retriever):
    @tool
    def search_products(query: str) -> str:
        """
        当用户询问产品信息、价格、售后、库存或发货政策时使用。
        """
        docs = retriever.invoke(query) # 内部含CRAG优化逻辑 [cite: 25, 26]
        res = []
        for d in docs:
            # 确保包含链接和图片信息 [cite: 40]
            res.append(f"信息: {d.page_content}\n来源: {d.metadata.get('url', '商城详情页')}")
        return "\n\n".join(res)
    return search_products

# 3. 构造 Agent 执行器
def get_agent_executor():
    # 初始化 RAG 检索器
    retriever = init_retriever()
    
    # 设定 LLM (对应导图：大语言模型) [cite: 38]
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)
    
    # 定义工具集
    tools = [query_express_track, create_knowledge_tool(retriever)]
    
    # 预设 Prompt (核心约束) [cite: 32, 33, 34, 35]
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一位电商金牌客服。
        1. **语气**：必须活泼、热情，尽可能多使用表情包 😊🛍️。
        2. **限制**：响应必须简洁，严格控制在300字以内 [cite: 35]。
        3. **范围**：仅回答电商、产品及物流相关问题。若提问无关，请礼貌拒绝并温馨提醒 。
        4. **展示**：提及产品时，请务必附带提供的链接和图片信息 [cite: 40]。
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # 创建 Agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
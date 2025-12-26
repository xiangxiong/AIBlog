'''
阶段三的高级挑战：Memory（记忆）
Agent 最大的问题是“健忘”。如果你想做一个能和你聊天、记得你上一句话说的是什么的机器人，你需要加入 ChatMessageHistory。
'''
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek


load_dotenv();

model = ChatDeepSeek(model="deepseek-chat", temperature=0);
parser = StrOutputParser()

# 1. 模拟一个简单的对话
memory_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手。"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
]);

chain = memory_prompt | model | parser;


# 2. 包装记忆逻辑
store = {}; # 实际开发中可以换成 Redis
def getSessionHistory(sessionId:str):
    if sessionId not in store:
        store[sessionId] = ChatMessageHistory();
    return store[sessionId];

# 3. 创建带记忆的对话链
withMemoryChain = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=getSessionHistory,
    input_messages_key="input",
    history_messages_key="chat_history",
);

# 3. 连续对话
config = {"configurable": {"session_id": "user_001"}}
print(withMemoryChain.invoke({"input": "你好，我叫小明"}, config=config))
print(withMemoryChain.invoke({"input": "我还记得我叫什么吗？"}, config=config))




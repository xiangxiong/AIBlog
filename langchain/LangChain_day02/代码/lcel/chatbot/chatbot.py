#自动会话历史管理组件RunnableWithMessageHistory
#以及如何流式处理大模型的应答
import os

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
from langchain_core.tracers import LangChainTracer, ConsoleCallbackHandler
from langsmith import traceable

from models import get_lc_model_client



# 用户输入 + config.session_id → 找到 Redis 中的历史记录 → 和当前输入一起发给模型 → 生成回答 → 把回答存回 Redis。

client = get_lc_model_client()

#定义提示模版
# 没有手动插入上下文
prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("你是一个聊天助手，用中文回答所有的问题"),
        HumanMessagePromptTemplate.from_template("{input}"),
        # ("human", "{input}"),
    ]
)
parser = StrOutputParser()
# 以链的形式
chain = prompt_template | client | parser

''' 
#ttl 当前会话数据的过期时间，300秒表示5分钟过期
chat_message_history = RedisChatMessageHistory(url=REDIS_URL, session_id=session_id, ttl=300)
'''
# history = RedisChatMessageHistory(session_id="my_session_id", url="redis://localhost:6379")



def get_session_history(session_id):
    return RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379",
        ttl=300  # 300秒表示5分钟过期，这个添加记忆持续时间 5分钟
    )

# 串联历史记录（记忆） 和 链
# 将对话历史自动集成到模型调用链中，解决了聊天机器人在上下文连续性
# 和多用户支持中的核心问题
chatbot_with_his = RunnableWithMessageHistory(
    # 执行流程
    chain,
    # 记忆存储的位置的函数
    get_session_history,
    input_messages_key="input",
)

# 模拟了两个用户的会话 ，"session_id": "用户的唯一标识"
# user123对话
resp_user123 = chatbot_with_his.invoke(
    {"input": "我是user123,我喜欢音乐，你能给我推荐一首轻音乐吗？"},
        # config 配置信息 configurable  {"session_id": "user123"} 配置的是用户的身份信息
        config={
            "configurable": {"session_id": "user123"},
        },

)
# 大模型回复
print("用户123的回答：", resp_user123)
print("==================")
# jack对话
resp_jack = chatbot_with_his.invoke(
    {"input": "我是jack,我热爱运动，篮球是我的最爱，你猜我喜欢哪个NBA球星？"},
    config={"configurable": {"session_id": "jack"}}
)
print("用户jack的回答：", resp_jack)
print("==================")
# user123再次提问
resp1_user123 = chatbot_with_his.invoke(
    {"input": "我喜欢什么？"},
    config={"configurable": {"session_id": "user123"}}
)
print("用户123的回答：", resp1_user123)

print("==================")
resp_jack1 = chatbot_with_his.invoke(
    {"input": "我喜欢什么？"},
    config={"configurable": {"session_id": "jack"}}
)
print("用户jack的回答：", resp_jack1)



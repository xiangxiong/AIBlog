#消息历史组件ChatMessageHistory的使用

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
import sys
from pathlib import Path

from models import  get_ali_model_client

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("你是人工智能助手"),
        # 作用就是向提示词中插入一段上下文消息
        # ("placeholder", "{messages}"),
        MessagesPlaceholder(variable_name="messages"),  #QA QA
        # HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

client = get_ali_model_client()

parser = StrOutputParser()
chain =  chat_template | client | parser

#  创建消息历史记录，存储组件
chat_history = ChatMessageHistory()

# add_user_message() 添加用户的输入信息
# add_ai_message() 添加存储大模型的回复信息
# .messages 属性获取所有历史消息

while True:
    user_input = input("用户：")
    if user_input == "exit":
        break

    # 添加用户输入
    chat_history.add_user_message(user_input)
    # 访问LLM时，chat_history.messages 获取所有的历史消息
    response = chain.invoke({'messages': chat_history.messages})

    print("chat_history:",chat_history.messages)
    print(f"大模型回复》》》：{response}")

    # 将大模型的回复加入历史记录
    chat_history.add_ai_message(response)


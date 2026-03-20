#展示大模型的无状态，记不住我们聊天中每次的对话内容
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

from models import get_lc_model_client

# 直接访问LLM
client = get_lc_model_client()

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("你是人工智能助手"),
        ('human', '{text}')
    ]
)
parser = StrOutputParser()

chain = chat_template | client | parser

while True:
    user_input = input("请输入 'quit' 退出程序: ")
    if user_input == 'quit':
        print("程序结束。")
        break
    else:
        print(chain.invoke({'text': user_input}))

# # 问题1
# print(chain.invoke({'text': '你好，我是大白'}))
# # 问题2
# print(chain.invoke({'text': '你好，我是谁？'}))

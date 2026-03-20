from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

#1.模型客户端,streaming对话采样流式输出
model = ChatTongyi(streaming=True)

#2.构建提示词模板
prompt = PromptTemplate(
    input_variables=["topic"],
    template="用5句话来介绍{topic}"
)

#3.结果解析器
out = StrOutputParser()

#4.构建链式调用
chain = prompt | model | out
# print(chain.invoke({"topic": "人工智能"}))
for chunk in chain.stream({"topic": "人工智能"}):
    print(chunk, end="", flush=True) #flush=True 刷新缓冲区
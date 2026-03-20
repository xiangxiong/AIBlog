from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

#1.模型客户端
model = ChatTongyi()

#2.构建提示词模板
prompt = PromptTemplate(
    input_variables=["topic"],
    template="用5句话来介绍{topic}"
)

#3.结果解析器
out = StrOutputParser()
# 顺序执行每一个节点
chain = RunnableSequence(prompt,model,out)
# chain = prompt | model | out
print(chain.invoke({"topic": "人工智能"}))
from langchain_core.prompts import ChatPromptTemplate
# 创建解析器
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from models import get_lc_model_client

#获得访问大模型客户端
client = get_lc_model_client()
# output_parser = StrOutputParser()
output_parser = JsonOutputParser()

# 提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的程序员"),
    ("user", "{input}")
])

# 将提示和模型合并以进行调用
chain = prompt | client | output_parser


#明确告诉大模型用JSON格式返回，我们可以用JSONOutputParser获得JSON格式的内容以进行后续处理，否则返回一个字符串
result = chain.invoke({"input": "langchain是什么? 问题用question 回答用ans 返回一个JSON格式"})
print(type(result))
print(result)
# print(chain.invoke({"input": "大模型中的langchain是什么?"}))


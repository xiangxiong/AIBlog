from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# 1.创建模型客户端
model = ChatTongyi()
#2.构建提示词，访问模型
# prompt = "你是谁？"
# 字符串提示词模板 {text}  占位符，通过text变量动态设置提示词内容
prompt = PromptTemplate(template="你是一个翻译助手，请讲以下内容翻译成{language}:{text}")

# 输入参数内容，构建真正的提示词
# fact_prompt = prompt.format(language="中文", text="I am a programmer")
# print(fact_prompt)
parser = StrOutputParser()

#
# result = model.invoke(fact_prompt)
# #3.获取打印结果
# # print(result.content)
# # 4.字符串结果解析器，解析：作用 将大模型返回的内容，获取到字符串内容返回

# str = parser.invoke( result) # 字符串解析
# print(str)
# 链的调用   在langchain中  "|" 是一个链的调用符
chain = prompt | model | parser
result = chain.invoke({"language": "中文", "text": "I am a programmer"})
print(result)

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate

# 作用这是参数，提前先设置一个参数，后续在设置其他参数，分开给不同参数赋值
# 比如：实现学习助手，在提问前先设置学科，在输入内容问题

# 1.创建模型客户端
model = ChatTongyi()
#2.构建提示词，访问模型
# prompt = "你是谁？"
# 字符串提示词模板 {text}  占位符，通过text变量动态设置提示词内容
prompt_txt = "讲一个关于{date}的小故事：{text}"

prompt = PromptTemplate(template=prompt_txt, input_variables=["date", "text"])

# 输入参数内容，构建真正的提示词
half_prompt = prompt.partial(date="2008-08-08")

print(half_prompt)


result = model.invoke(half_prompt.format(text="一个幸福的爱情故事"))
#3.获取打印结果
print(result.content)

result = model.invoke(half_prompt.format(text="一个悲伤的爱情故事"))
#3.获取打印结果
print(result.content)
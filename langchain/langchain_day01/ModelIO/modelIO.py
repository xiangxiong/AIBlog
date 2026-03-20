import os

from langchain.chat_models import init_chat_model
from langchain_community.chat_models import ChatTongyi
from langchain_openai import ChatOpenAI

#1.创建模型客户端,访问基于openai规范的一类模型
# api_key 模型key  model:模型名称  base_url：模型链接的链接地址
# model = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),model="qwen-max",base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
#1.2 其他方式 ，不是openAI兼容的 查看源码：ctrl+鼠标左击
# model = init_chat_model(model="deepseek-chat" ,model_provider="deepseek" )
#1.3 基于某个平台模型
model = ChatTongyi()
#2.构建提示词，访问模型
prompt = "你是谁？"
result = model.invoke(prompt)
#3.获取打印结果
print(result.content)
import os
from openai import OpenAI

# 传统方式跟大模型交互
# 创建大模型连接
# client = OpenAI(
#     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# )
# completion = client.chat.completions.create(
#     model="qwen-max",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#     messages=[
#         {'role': 'system', 'content': 'You are a helpful assistant.'},
#         {'role': 'user', 'content': '你是谁？'}],
# )
# # print(completion.model_dump_json())
# print(completion.choices[0].message.content)


# 使用Langchain方式交互
from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi()

response = model.invoke("你是谁？")
print(response.content)
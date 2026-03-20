from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

# 传统方式跟大模型交互
# 创建大模型连接
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)
completion = client.chat.completions.create(
    model=DEEPSEEK_MODEL,
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}],
)
# print(completion.model_dump_json())
print(completion.choices[0].message.content)

# 使用 Langchain 方式交互
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    openai_api_key=DEEPSEEK_API_KEY,
    openai_api_base=DEEPSEEK_BASE_URL,
    model_name=DEEPSEEK_MODEL
)

response = model.invoke("你是谁？")
print(response.content)

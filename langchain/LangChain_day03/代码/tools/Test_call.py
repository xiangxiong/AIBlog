import datetime
import os

from dashscope import api_key
from langchain.agents import create_agent

from langchain_openai import ChatOpenAI
from langchain.chat_models import  init_chat_model
from langchain_core.prompts import  PromptTemplate
# from langchain_core.tools import tool
from langchain.tools import tool


# api_key  秘钥  model：模型名称 base_url：模型连接的url地址
model = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen-max", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# 注意：函数的描述必须写在函数体中的第一行
@tool
def get_date():
    """ 获取今天的具体日期 """
    # """ 获取今天的北京的天气 """
    return datetime.date.today().strftime("%Y-%m-%d")


import webbrowser
@tool
def open_browser(url, browser_name=None):
    """ 获取浏览器，打开网站 """
    if browser_name:
        # 获取特定浏览器的控制器
        browser = webbrowser.get(browser_name)
    else:
        # 使用默认浏览器
        browser = webbrowser
    # 打开浏览器并导航到指定的URL
    browser.open(url)

# 大模型客户端绑定工具
agent = create_agent(
    model,
    tools=[get_date, open_browser],
)
# 执行agent
# result = agent.invoke({"messages":[{"role":"user","content":"帮我打开淘宝"}]})
# result = agent.invoke({"messages":[{"role":"user","content":"今天是几月几号？"}]})
# 获取北京的今天的天气
result = agent.invoke({"messages":[{"role":"user","content":"帮我打开淘宝"}]})
print( result)



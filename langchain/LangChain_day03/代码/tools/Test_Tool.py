import datetime
import os

from dashscope import api_key

from langchain_openai import ChatOpenAI
from langchain.chat_models import  init_chat_model
from langchain_core.prompts import  PromptTemplate
# from langchain_core.tools import tool
from langchain.tools import tool


# api_key  秘钥  model：模型名称 base_url：模型连接的url地址
model = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen-max", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# resp = model.invoke("今天北京的天气是怎么样的？")
# resp = model.invoke("今天是几月几号？")
# print(resp)
# exit()

@tool
def get_date():
    """ 获取今天的具体日期 """
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
tool_llm = model.bind_tools([get_date, open_browser])
# tool_llm = model.bind_tools([get_date])
resp = tool_llm.invoke("今天是几月几号？")

# resp = tool_llm.invoke("帮我访问淘宝网站？")

# 大模型给的回复，不是结果，而是通过大模型分析，判断哪个工具能解决当前提问（工具选择）
# 就是通过工具定义时，描述
print(resp)
print("---"*20)

# all_tools= {
#     "get_date": get_date,
#     "open_browser": open_browser
# }
# 大模型给函数调用的筛选结果，并没有直接调用工具
# 手动执行调用函数的过程
# if resp.tool_calls:
#     for tool_call in resp.tool_calls:
#         tool = tool_call["name"]
#         print(tool)
#         print(tool_call["args"])
#         # 从字典中获取工具函数体
#         selected_tool = all_tools.get(tool)
#         # 手动执行函数
#         result = selected_tool.invoke(tool_call["args"])
#         print(result)



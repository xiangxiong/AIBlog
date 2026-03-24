import gradio as gr
import os
import json
import random
import subprocess
import webbrowser
from datetime import datetime
from http import HTTPStatus
from typing import List, Dict, Any

from langchain.agents import create_agent
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.tools import Tool

from langchain_openai import ChatOpenAI


import sys
from pathlib import Path

# 允许直接运行当前脚本时，导入上层目录中的 models.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from models import get_ds_model_client
from dotenv import load_dotenv

load_dotenv()

# api_key  秘钥  model：模型名称 base_url：模型连接的url地址
# model = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen-max", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

llm = get_ds_model_client(model="deepseek-chat")


# 定义工具函数
def get_current_time(input: str = "") -> str:
    """获取当前时间"""
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    result = f"当前时间：{formatted_time}。"
    print(result)
    return result


def recom_drink(input: str = "") -> str:
    """推荐附近的饮品店"""
    result = '''距离您500米内有如下饮料店：\n
    1、蜜雪冰城\n
    2、茶颜悦色\n
    另外距离您200米内有惠民便利店，里面应该有矿泉水或其他饮品'''
    return result


def open_calc(input: str = "") -> str:
    """打开计算器"""
    try:
        subprocess.Popen(['calc.exe'])
        return "计算器已打开"
    except Exception as e:
        return f"打开计算器失败: {str(e)}"


def open_browser(url: str) -> str:
    """打开浏览器访问指定网址"""
    try:
        webbrowser.open(url)
        return f"已打开浏览器访问 {url}"
    except Exception as e:
        return f"打开浏览器失败: {str(e)}"


# 初始化聊天模型和记忆
# llm = ChatOpenAI(
#     openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
#     openai_api_key=os.getenv("DASHSCOPE_API_KEY"),
#     model_name="qwen-max"
# )
# 创建提示模板
system_prompt = "你是人工智能助手。需要帮助用户解决各种问题。"

# 创建记忆
# 短期记忆构建：智能体中使用InMemorySaver()实现单会话的短期记忆
from langgraph.checkpoint.memory import InMemorySaver
# 创建短期记忆实例
memory = InMemorySaver()

# 创建LangChain工具列表
# 方式二，自定义工具
tools = [
    # 通过Tool来描述声明工具 name 工具名称 func 函数体 description 函数的功能描述
    Tool(
        name="get_current_time", #可以随意，但是建议跟函数名称一致
        func=get_current_time,
        # 函数的功能描述，说明书
        description="当你想知道现在的时间时非常有用。"
    ),
    Tool(
        name="recom_drink",
        func=recom_drink,
        description="用户口渴，为其推荐附近的饮品店"
    ),
    Tool(
        name="open_calc",
        func=open_calc,
        description="打开本地计算机上的计算器。"
    ),
    Tool(
        name="open_browser",
        func=lambda url: open_browser(url),
        description="打开本地计算机上的网页浏览器，并接受网站的url作为参数。"
    )
]


# 这个时候函数工具选择和调用执行，都是通过Agent来完成的
# 创建Agent
agent = create_agent(
    model=llm,  # 聊天模型
    tools=tools, # 工具列表
    system_prompt=system_prompt,
    checkpointer=memory  # 传入记忆组件
)

# agent = initialize_agent(
#     tools, # 工具列表
#     llm, # 聊天模型
#     agent=AgentType.OPENAI_FUNCTIONS,
#     verbose=True,
#     memory=memory, # 记忆
#     agent_kwargs=agent_kwargs,
#     handle_parsing_errors=True
# )

# 本地测试调用工具
# RAG  调用工具  一个是最新数据大模型不知道     私有的数据大模型不知道
# response = agent.invoke(
#             {"messages": [{"role": "user", "content": "我想用计算器计算？"}]},
#             # 配置会话标识，用于区分不同用户
#             config={"configurable": {"thread_id": "user_1"}}  # 会话唯一标识，用于区分不同用户
#         )
# print(response)
# exit()



# 与前端交互处理LLM响应
def process_llm_response(query, show_history):
    if len(query) == 0:
        return show_history + [("", "")]
    try:
        # 显示用户查询和等待提示
        yield show_history + [(query, "正在查询大模型...")],""

        # 使用Agent处理查询
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            # 配置会话标识，用于区分不同用户
            config={"configurable": {"thread_id": "user_1"}}  # 会话唯一标识，用于区分不同用户
        )
        print(f"LLM输出：{response}")

        # 正确提取回答内容 - 只显示output部分
        if isinstance(response, dict) and 'messages' in response:
            response = response["messages"][-1].content
        else:
            # 如果response不是预期的字典格式，尝试提取其他可能的字段
            response = str(response)
            print(f"警告: 响应格式异常: {response}")

        # 返回结果
        yield show_history + [(query, response)],""
    except Exception as e:
        print(f"Error: {e}")
        yield show_history + [(query, "AI助手出错，请重试或者检查")]



# 前端界面展示
with gr.Blocks(title="大模型中Function Call演示") as demo:
    gr.HTML('<center><h1>欢迎大模型中Function Call演示</h1></center>')

    with gr.Row():
        with gr.Column(scale=10):
            chatbot = gr.Chatbot(height=650)  # 空初始值

    with gr.Row():
        msg = gr.Textbox(label="输入", placeholder="您想了解什么呢？")

    with gr.Row():
        examples = gr.Examples(
            examples=[
                '请问如何做红烧牛肉？',
                '料酒可以换成白酒吗？',
                '帮我打开计算器',
                '现在几点了？',
                '帮我访问淘宝网',
                '我渴了'
            ],
            inputs=[msg]
        )

    clear = gr.ClearButton([chatbot, msg])
    msg.submit(process_llm_response, [msg, chatbot], [chatbot,msg])


if __name__ == '__main__':
    demo.launch(server_port=7778)
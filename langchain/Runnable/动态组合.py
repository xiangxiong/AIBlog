
# 核心目标: 学习如何在一个链中并行处理数据。这在后面做 RAG（检索增强生成）时非常关键.
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough,RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek

# 加载环境变量
load_dotenv()

# 1. 定义模型
model = ChatDeepSeek(model="deepseek-chat", temperature=0)

# # 定义简单的同步函数作为模型和解析器的替代
# def mock_model(inputs):
#     if "总结" in inputs.messages[0].content:
#         return {"content": "这是一个关于LangChain框架的总结。"}
#     else:
#         return {"content": "This is an introduction to LangChain framework."}
# def mock_parser(inputs):
#     return inputs["content"]

# 初始化模拟组件
parser = StrOutputParser()

print("正在初始化...",parser)

# 假设我们要同时完成两个任务: 翻译 + 总结
summary_prompt = ChatPromptTemplate.from_template("用一句话总结{text}")
translate_prompt = ChatPromptTemplate.from_template("翻译成英文{text}")

# 构建并运行处理链
combined_chain = RunnableParallel(
    summary = summary_prompt | model | parser,
    translate = translate_prompt | model | parser
)

# 运行
result = combined_chain.invoke({"text":"LangChain 是一个旨在简化使用大语言模型创建应用程序的框架。它提供了链、代理等核心概念。"})
print(result)




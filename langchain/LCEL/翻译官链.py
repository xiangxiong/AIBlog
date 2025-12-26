from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek

# 加载环境变量
load_dotenv()

# 1. 定义模型
model = ChatDeepSeek(model="deepseek-chat", temperature=0)

# 2. 定义prompt
prompt = PromptTemplate.from_template("将以下内容翻译成英文：{text}")

# 3. 定义输出解析器
parser = StrOutputParser()

# 4. 构建链(LCEL)
chain = prompt | model | parser

# 5. 调用
print(chain.invoke({"text": "我正在通过实战快速学习 LangChain"}))

'''
1、| 符号的作用是把前一步的输出自动传给下一步的输入。
2、 StrOutputParser() 非常重要，它让你拿到的直接是结果文本，而不是一大串包含 Token 信息的 JSON#
'''
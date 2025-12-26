from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatDeepSeek

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
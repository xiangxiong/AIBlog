from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek
from langchain_core.runnables import RunnableLambda

load_dotenv()

model = ChatDeepSeek(model="deepseek-chat", temperature=0)

parser = StrOutputParser()

def length_check(text):
    return "这段文字太短了,请多写一点" if len(text) < 10 else text

combine_chain = RunnableLambda(length_check) | model | parser

print(combine_chain.invoke("你好"));


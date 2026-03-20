#学会利用LangChain部署我们的应用成为WEB服务


from fastapi import FastAPI
from langchain_community.chat_models import ChatTongyi
from langchain_core.globals import set_debug

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langserve import add_routes

from models import get_lc_model_client
# 开启调试
set_debug(True)

#获得访问大模型客户端
# client = ChatTongyi()
client = get_lc_model_client()

#解析返回结果
parser = StrOutputParser()

#定义提示模版
prompt_template = ChatPromptTemplate.from_messages(
    [
        #改为 ('system','请将以下的内容翻译成{language}') 也可以
        SystemMessagePromptTemplate.from_template("请将以下的内容翻译成{language}"),
        # 改为 HumanMessagePromptTemplate.from_template("{text}") 也可以
        ('human', '{text}')
    ]
)

# 以链的形式调用
chain = prompt_template | client | parser

# 本地调用  chain.invoke({language:'',text:''}})
# print(chain.invoke({"language": '中文', "text": "hello"}))


#部署为服务  部署成web应用的框架
app = FastAPI(title="基于LangChain的服务",version="V1.5",description="翻译服务")
# 函数和访问路径一一对应
add_routes(app, chain,path="/lanchainServer")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
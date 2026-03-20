from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models import get_lc_model_client, get_ali_model_client

#获得访问大模型客户端
client = get_ali_model_client()

# 创建提示模板
prompt = ChatPromptTemplate.from_messages(
    [
     ("system", "根据提供的上下文: {context} \n\n 回答问题"),
     ("user", "问题：{input}"),  # 用户输入的问题
     ]
)

# 构建链  这个链将文档作为输入，并使用之前定义的提示模板和初始化的大模型来生成答案
# 链要求输入是一个字典，必须包含context,默认就是将context中的内容作为文档给大模型
chain = create_stuff_documents_chain(client, prompt)

# create_sql_query_chain

# 加载文档  bs :Beautiful Soup 解析器 工具，进行内容分割的工具
loader = WebBaseLoader(
        web_path="https://www.gov.cn/yaowen/liebiao/202512/content_7050416.htm",
        # bs_kwargs=dict(parse_only=bs4.SoupStrainer(id="UCAP-CONTENT"))
        # 分割，将网页中目标内容进行分割
        bs_kwargs={"parse_only":bs4.SoupStrainer(id="UCAP-CONTENT")}
        )

docs = loader.load()

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
documents = text_splitter.split_documents(docs)
# print(documents)
print(len(documents))

# 执行链  检索  民事法律行为? 出来的结果
res = chain.invoke({"input": "会议具体说了哪些内容?", "context": documents})
print(res)
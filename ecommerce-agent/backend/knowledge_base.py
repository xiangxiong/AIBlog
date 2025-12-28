import json
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI

def init_retriever():
    # 加载 JSON 格式知识库 [cite: 17]
    with open("data/knowledge.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    texts = [f"商品:{i['title']} 价格:{i['price']} 售后:{i['after_sales']}" for i in data]
    # 设置 Token 块大小 [cite: 17, 19]
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.create_documents(texts)
    
    vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
    
    # CRAG 优化：剔除无关数据 [cite: 25, 26]
    llm = ChatOpenAI(temperature=0)
    compressor = LLMChainExtractor.from_llm(llm)
    
    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vectorstore.as_retriever()
    )
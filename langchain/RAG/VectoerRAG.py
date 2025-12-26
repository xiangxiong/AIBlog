from langchain.embeddings.vectorstore import FAISS
from langchain_core import OpenAIEmbeddings
from langchain_text_splitter import RecursiveCharacterTextSplitter

# 构建你的第一个，本地知识库.
# 核心目标： 理解文本是如何变成向量并存进数据库的.

# 1.原始长文本 (模拟你的文档)
raw_text = """
LangChain 实战指南：
1. LCEL 是核心语法。
2. RAG 是目前最火的落地场景。
3. Agent 代理是未来的高级形态。
"""

# 2. 切分文档(把大书拆成小页)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.create_documents([raw_text])

# 3. 向量化并存储到本地 (把文字变成 AI 能懂的数字坐标)
# 注意：这步会调用 OpenAI 的 Embedding 接口，需要消耗微量 Token
vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())

# 4. 存为本地索引文件，下载直接加载
vectorstore.save_local("vectorstore")
print("知识库已成功建立！")
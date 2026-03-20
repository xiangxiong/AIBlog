import os
# 安装 pip install langchain_chroma
# 加载word文档 安装 pip install docx2txt
# 加载json文档 安装 pip install jq
# 加载pdf文档  安装 pip install pymupdf
# 加载HTML文档 安装 pip install unstructured
# 加载MD文档   安装 pip install markdown +  pip install unstructured
import langchain
from langchain_community.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models import get_lc_model_client, ALI_TONGYI_API_KEY_OS_VAR_NAME, ALI_TONGYI_EMBEDDING_MODEL, get_ali_model_client


#获得访问大模型客户端
client = get_ali_model_client()

#直接了解LangChain中的“文档”(Document)的具体内容，这里我们跳过了文档与文档加载，文档切割和文档转换过程
#文档的模拟数据
#  page_content 存储原始文档内容  metadata（元数据） 存储当前文档描述信息
# documents = [
#     Document(
#         page_content="猫是柔软可爱的动物，但相对独立",
#         metadata={"source": "常见动物宠物文档"},
#     ),
#     Document(
#         page_content="狗是人类很早开始的动物伴侣，具有团队能力",
#         metadata={"source": "常见动物宠物文档"},
#     ),
#     Document(
#         page_content="金鱼是我们常常喂养的观赏动物之一，活泼灵动",
#         metadata={"source": "鱼类宠物文档"},
#     ),
#     Document(
#         page_content="鹦鹉是猛禽，但能够模仿人类的语言",
#         metadata={"source": "飞禽宠物文档"},
#     ),
#     Document(
#         page_content="兔子是小朋友比较喜欢的宠物，但是比较难喂养",
#         metadata={"source": "常见动物宠物文档"},
#     ),
# ]

from langchain_community.document_loaders import UnstructuredWordDocumentLoader, Docx2txtLoader

# 1.指定要加载的Word文档路径
loader = Docx2txtLoader("人事管理流程.docx")

# 加载文档、转换格式化成document
documents = loader.load()
# print(len(documents))
# # Document(metadata={'source': '人事管理流程.docx'}, page_content='集团管理制度\n\n人')
# print(documents)

# 文档切割 递归切割
# separators
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, #切块大小
    chunk_overlap=50,  # 切块重叠大小
    # separators=[".", '\n', '!', '?', ';']
)
# 通过分割器获取document :create_documents   split_documents  传入一个document对象，返回一个document对象列表
split_documents = text_splitter.split_documents(documents)

# 模型包装器：大模型分成三类：LLM  聊天模型  嵌入模型
# 获得一个阿里通义千问嵌入模型的实例，同样在models.py中被包装为get_ali_embeddings()
from langchain_community.embeddings import DashScopeEmbeddings
# 嵌入模型的模型包装器
llm_embeddings = DashScopeEmbeddings(
    # 模型名称
    model=ALI_TONGYI_EMBEDDING_MODEL,
    # API_KEY
    dashscope_api_key=os.getenv(ALI_TONGYI_API_KEY_OS_VAR_NAME)
)

# 实例化向量空间，向量化+向量存储到向量数据库中
vector_store = Chroma.from_documents(documents=split_documents,embedding=llm_embeddings)


#展示相似度查询，实际业务中可以不要
# print(vector_store.similarity_search("狸花猫"))
# print("--"*15)
# print(vector_store.similarity_search_with_score("狸花猫"))


# print(vector_store.similarity_search("晋升"))
# 从向量数据库检索出来的结果

#按相似度的分数进行排序，分数值越小，越相似（其实是L2距离）
#从向量数据库检索，使用chroma原始API查询   bind(k=1)表示返回相似度最高的第一个 top-K
# print(vector_store.similarity_search_with_score("晋升"))
#
# exit()

# 检索器对象：检索文档，可以根据需要对检索后的结果做各种处理
# VectorStoreRetriever 中allowed_search_types 参数设置检索方式：
# "similarity", 默认，向量相似度检索
# "similarity_score_threshold", 向量相似度阈值检索
# "mmr"  max margin relevance :一种平衡相关性和多样性的检索方式
# 每一组中只会选择一个结果，同组的结果丢弃掉  topk=4
# 人工智能应用场景？    排1-2-5的全部是医疗相关的应用 6-8 金融相关  法律
# 步骤：
# 1.从知识库检索出一个候选文档集合
# 2.从候选集中迭代的选择文档，选择一个后，计算边际相关性分数（文档本身与原始查询相似性，与已经选择的结果的相似度高则排除--惩罚冗余，鼓励多样性）
# 应用场景：1.摘要任务  2.问答系统  3.推荐系统
# 默认top-k=4
retriever = vector_store.as_retriever()
# retriever = vector_store.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={
#         "score_threshold": 0.3,
#     }
# )
#
# result = retriever.invoke("晋升")
#
# print(result)
#
#
# exit()

message = """ 
仅使用提供的上下文回答下面的问题：
{question}
上下文：
{context}
"""
prompt_template = ChatPromptTemplate.from_messages([('human',message)])
# 定义这个链的时候，还不知道问题是什么，
# 用RunnablePassthrough允许我们将用户的具体问题在实际使用过程中进行动态传入
chain = {"question":RunnablePassthrough(),"context":retriever} | prompt_template | client

#用大模型生成答案
resp = chain.invoke("晋升")
print(resp.content)

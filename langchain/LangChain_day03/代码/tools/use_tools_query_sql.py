import os
from operator import itemgetter

from langchain_classic.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_community.utilities import SQLDatabase

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import re
from models import get_lc_model_client, get_ali_model_client, ALI_TONGYI_MAX_MODEL

#langchain.debug = True

# 使用工具，将自然语言转换成sql,并且执行sql,将查询的结果给模型，然后大模型回复

#获得访问大模型客户端
client = get_ali_model_client(model=ALI_TONGYI_MAX_MODEL)

#数据库配置 pip install mysqlclient      mysqlclient==2.2.7
HOSTNAME ='127.0.0.1'
PORT ='3306'
DATABASE = 'world'
USERNAME = 'root'
PASSWORD ='1234'
MYSQL_URI ='mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
db = SQLDatabase.from_uri(MYSQL_URI)
# 获取数据库中所有的表名称
# print(db.get_usable_table_names())
# # 执行sql的函数
# print(db.run('select * from country limit 1'))
#
# exit()


#2、因为实际产生的sql是形如```sql....```的，无法直接执行，所以需要清理
#自定义一个输出解析器SQLCleaner
class SQLCleaner(StrOutputParser):
    def parse(self, text: str) -> str:
        pattern = r'```sql(.*?)```'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sql = match.group(1).strip()
            # 某些大模型还会产生类似'SQLQuery:'前缀，必须去除
            sql = re.sub(r'^SQLQuery:', '', sql).strip()
            return sql
        # 某些大模型还会产生类似'SQLQuery:'前缀，必须去除
        text = re.sub(r'^SQLQuery:', '', text).strip()
        return text



# 1.预定义的链，通用的功能，langchain已经将实现流程固定，代码已经定义好
sql_make_chain = create_sql_query_chain(client, db)| SQLCleaner()

# resp = sql_make_chain.invoke({"question":"请从国家表中查询出China的相关数据"})
# resp = sql_make_chain.invoke({"question":"请从城市表中查询出Haag的相关数据"})
#
# print("实际可用SQL: ",resp)
# print("**"*15)
# exit()

#3、将前面的部分组合起来，得到最终结果
answer_prompt = PromptTemplate.from_template(
    """给定以下用户问题、可能的SQL语句和SQL执行后的结果，回答用户问题
    Question: {question}
    SQL Query: {query}
    SQL Result:{result}
    回答:"""
)
#2.创建一个执行SQL的工具
execute_sql_tools = QuerySQLDatabaseTool(db = db)
# runnable = RunnablePassthrough.assign(query=sql_make_chain)
# print("RunnablePassthrough-1：",runnable.invoke({"question":"请从国家表中查询出China的相关数据"}))
#
# runnable = RunnablePassthrough.assign(query=sql_make_chain)| itemgetter('query')
# print("RunnablePassthrough-2：",runnable.invoke({"question":"请从国家表中查询出China的相关数据"}))
#
# runnable = RunnablePassthrough.assign(query=sql_make_chain)| itemgetter('query') | execute_sql_tools
# print("RunnablePassthrough-3：",runnable.invoke({"question":"请从国家表中查询出China的相关数据"}))
#
# runnable = RunnablePassthrough.assign(query=sql_make_chain).assign(result=itemgetter('query')|execute_sql_tools)
# print("RunnablePassthrough-4：",runnable.invoke({"question":"请从国家表中查询出China的相关数据"}))
#
# exit()
'''通过上面的步骤，就能搞清楚{question}、{query}、{result}这三个字段是如何通过LCEL链一步步获得的
要注意的是result=itemgetter('query')|execute_sql_tools 中，执行顺序是：
itemgetter('query') -> execute_sql_tools -> result=
所以这段代码实际是：result=(itemgetter('query')|execute_sql_tools)'''
chain = (RunnablePassthrough.assign(query=sql_make_chain).assign(result=itemgetter('query')|execute_sql_tools)
         # {question：问题，query：sql , result : 结果}
        |answer_prompt| client| StrOutputParser())


result = chain.invoke(input={"question":"请从国家表中查询出China的相关数据"})
#result = chain.invoke(input={"question":"请问国家表中有多少条数据"})
print("最终执行的结果：",result)
'''，如果场景是确定的，并不需要大模型来决定是否使用工具，直接在链中加入工具即可
#但是如果需要大模型来决定是否使用工具，比如场景是动态的或者是以工具组的形式提供工具，那么需要使用Function Call：'''
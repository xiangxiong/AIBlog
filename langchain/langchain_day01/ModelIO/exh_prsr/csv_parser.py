from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser
from models import get_lc_model_client

# 获得访问大模型客户端
# client = ChatTongyi();
client = get_lc_model_client()

# 创建解析器
# output_parser = StrOutputParser()
# 将返回结果列表返回，多个值用逗号分隔
output_parser = CommaSeparatedListOutputParser()

# 提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的程序员"),
    ("user", "{input}")
])

# 将提示和模型合并以进行调用
chain = prompt | client | output_parser

# 示例调用
#明确告诉大模型用用逗号分隔返回，我们可以用CommaSeparatedListOutputParser获得内容后以
# 列表的形式获得以进行后续处理，否则返回一个字符串
print(chain.invoke({"input": "列出Python的三个主要版本, 用逗号分隔"}))
print(chain.invoke({"input": "列举三个常见的机器学习框架, 用逗号分隔"}))
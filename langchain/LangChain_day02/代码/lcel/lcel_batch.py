from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import time

# 1. 创建LCEL链
chain = (
    ChatPromptTemplate.from_template("用一句话介绍{topic}")
    | ChatTongyi()
    | StrOutputParser()
)

# 2. 准备批量输入
topics = ["人工智能", "区块链", "量子计算", "基因编辑"]
inputs = [{"topic": topic} for topic in topics]  #[{"topic":value},{"topic":value},...]

# 3. 单次调用计时  串行执行，一个个主题执行
start = time.time()
single_results = [chain.invoke({"topic": topic}) for topic in topics]
single_time = time.time() - start

# 4. 批量调用计时
start = time.time()
# 注意事项
# API供应商可能有批量请求限制（如每分钟请求数）
# 输入列表中的所有字典必须有相同的键结构
# 批量处理不适合有状态的操作（如带记忆的对话链）

batch_results = chain.batch(inputs)  # 关键批量调用方法
batch_time = time.time() - start

# 5. 结果对比
print(f"\n=== 单次调用耗时: {single_time:.2f}s ===")
for i, res in enumerate(single_results):
    print(f"{topics[i]}: {res}")

print(f"\n=== 批量调用耗时: {batch_time:.2f}s (加速 {single_time/batch_time:.1f}x) ===")
for i, res in enumerate(batch_results):
    print(f"{topics[i]}: {res}")
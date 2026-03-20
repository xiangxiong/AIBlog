from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# 原样进行数据传递

# chain = RunnableParallel(
#     passed = RunnablePassthrough(),
# )

# 数据增强，增强后进行继续传递
chain = RunnableParallel(
    passed = RunnablePassthrough().assign(modified= lambda x: x["k1"]+"!!!"),
)

# 调用链
# print(chain.invoke(("hello world")))

# 增强调用，需要使用字典格式
print(chain.invoke({"k1": "hello world"}))
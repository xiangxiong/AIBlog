from langchain_core.globals import set_debug
from langchain_core.runnables import RunnableParallel, RunnableMap, RunnableLambda

set_debug( True)
def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

def mul_three(x: int) -> int:
    return x * 3

# 测试parallel并行执行
# 同时执行三个函数，输出结果以字段的形式返回{a=2,b=2,c=3}
# chain = RunnableParallel(
#     a=add_one,
#     b=mul_two,
#     c=mul_three,
# )

chain = RunnableMap(
    a=add_one,
    b=mul_two,
    c=mul_three,
)
# 调用链
print(chain.invoke(1)) #{a=2,b=2,c=3}

chain1 = RunnableLambda(add_one)


chain2 = chain1|RunnableParallel(
    a = mul_two,
    b = mul_three,
)

print(chain2.invoke(2))

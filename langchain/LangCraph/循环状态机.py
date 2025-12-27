from typing import TypedDict,Annotated,List
from langgraph.graph import StateGraph,END

# 1.定义"状态"： 这是在所有节点间共享的大脑存储空间

class State(TypedDict):
    messages: List[str]

# 2. 定义节点: 每个节点就是一个处理函数
def chatbot(state:State):
    # 这里可以放模型调用逻辑
    return {"messages": state["messages"] + ["AI: 我思考了一下..."]}

def critic(state:State):
    # 模拟一个审查节点
    return {"messages": state["messages"] + ["审查员: 内容合格"]}

# 3. 构建图
workflow = StateGraph(State)

# 添加节点
workflow.add_node("agent",chatbot)
workflow.add_node("reviewer", critic)

# 建立链接: agent -> reviewer -> 结束
workflow.set_entry_point("agent")
workflow.add_edge("agent", "reviewer")
workflow.add_edge("reviewer", END)

# 4. 编译并运行
app = workflow.compile()
final_state = app.invoke({"messages": ["用户: 你好"]})
print(final_state["messages"])
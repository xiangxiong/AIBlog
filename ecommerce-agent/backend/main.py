import uvicorn

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.chat_message_histories import ChatMessageHistory

app = FastAPI(title="智能客服")

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# 1. 定义接口数据模型
class ChatInput(BaseModel):
    sessionId: str
    question: str

# 2. 会话内存管理
history_store = {}

def getSessionHistory(sessionId:str):
    if sessionId not in history_store:
        history_store[sessionId] = ChatMessageHistory();  # 使用列表来存储会话历史
    return history_store[sessionId];


# 3. 初始化 Agent 执行流
# executor = get_agent_executor()

# 4. 路由定义
@app.get("/")
async def root():
    return {"message": " Ecommerce Agent API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
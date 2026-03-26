from fastapi import FastAPI
from langchain_openai import ChatOpenAI
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("Deepseek_Key")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

app = FastAPI()

model = ChatOpenAI(
    openai_api_key=DEEPSEEK_API_KEY,
    openai_api_base=DEEPSEEK_BASE_URL,
    model_name=DEEPSEEK_MODEL
)

@app.get("/")
def read_root():
    """根路由"""
    response = model.invoke("你是谁？")
    # response = {"message": "Hello, World!"}
    print(response.content)
    return response.content

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)


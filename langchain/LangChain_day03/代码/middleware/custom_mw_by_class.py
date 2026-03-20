import os

from dotenv import load_dotenv
from langchain.agents.middleware import before_model, wrap_model_call, AgentMiddleware
from langchain.agents.middleware import AgentState, ModelRequest, ModelResponse
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.runtime import Runtime
from typing import Any, Callable


class LoggingMiddleware(AgentMiddleware):
    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"即将调用模型： {len(state['messages'])} 个消息")
        return None

    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"模型返回消息: {state['messages'][-1].content}")
        return None

llm = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen-max",base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

agent = create_agent(
    model=llm,
    middleware=[LoggingMiddleware()],
)
result = agent.invoke(
    {
        "messages": [{"role": "user","content": "你好",}]
    }
)
print(result)
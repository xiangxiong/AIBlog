import os

from dotenv import load_dotenv
from langchain.agents.middleware import before_model, wrap_model_call
from langchain.agents.middleware import AgentState, ModelRequest, ModelResponse
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.runtime import Runtime
from typing import Any, Callable

# 前置，在调用模型前，执行这个函数
@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"即将调用模型： {len(state['messages'])} 个消息")
    return None

# wrap_model_call 环绕，在model调用前后都执行这个函数
@wrap_model_call
def round_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
        print(f"模型调用前置处理 request： request={request}")
        print(f"模型调用前置处理 handler： handler={handler}")
        result = handler(request)  # 调用模型

        print(f"模型调用后，模型返回结果： {result}")
        return result


llm = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen-max",base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

agent = create_agent(
    model=llm,
    # 按照列表顺序依次执行中间件
    middleware=[log_before_model, round_model],
)
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "你好",
            }
        ]
    }
)
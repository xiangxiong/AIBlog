# LangServe 入门指南

## 一、LangServe 简介

### 1.1 什么是 LangServe？

LangServe 是一个专为部署 LangChain 应用而设计的高性能服务框架，它能够将 LangChain 构建的各种语言模型应用快速转换为生产就绪的 API 服务。通过 LangServe，你可以轻松地将提示模板、链（Chain）和代理（Agent）等组件部署为 RESTful API，无需编写复杂的服务代码。

### 1.2 核心优势

- **一键部署**：只需一行代码即可将 LangChain 组件转换为完整的 API 服务
- **自动文档**：基于 FastAPI 自动生成交互式 API 文档（Swagger UI/ReDoc）
- **类型安全**：利用 Pydantic 和类型提示确保 API 输入输出的安全性
- **高性能**：基于 FastAPI 和 Uvicorn，支持异步处理和高并发
- **流式支持**：原生支持 LLM 的流式输出
- **易于扩展**：完全兼容 FastAPI 生态系统，可以轻松添加自定义路由和中间件

### 1.3 应用场景

- 将 LangChain 构建的聊天机器人部署为 API 服务
- 快速搭建 AI 驱动的工具链服务
- 为前端应用提供语言模型后端支持
- 构建微服务架构中的 AI 组件

## 二、安装与环境准备

### 2.1 安装依赖

bash

```bash
pip install langserve
```



### 2.2 前置要求

- Python 3.8+
- 熟悉 LangChain 基本概念（提示模板、链、代理等）
- 了解 FastAPI 基础知识（可选）

## 三、快速开始

### 3.1 部署一个简单的链服务

以下是一个将简单提示模板部署为服务的完整示例：

python运行

```python
# main.py
from fastapi import FastAPI
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langserve import add_routes

# 初始化 LangChain 组件
prompt = PromptTemplate(
    input_variables=["question"],
    template="请回答以下问题：{question}"
)
llm = OpenAI(temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

# 创建 FastAPI 应用
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="一个基于 LangChain 的问答服务",
)

# 添加 LangChain 链作为路由
add_routes(app, chain, path="/qa")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
```



### 3.2 运行服务

bash

```bash
python main.py
```



### 3.3 访问 API

服务启动后，可以通过以下方式访问：

#### 标准调用

bash

```bash
curl -X 'POST' \
  'http://localhost:8000/qa/invoke' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "什么是机器学习？"
}'
```



#### 流式调用

bash

```bash
curl -X 'POST' \
  'http://localhost:8000/qa/stream' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "什么是机器学习？"
}'
```



### 3.4 查看 API 文档

访问以下 URL 查看自动生成的交互式文档：

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## 四、核心概念与功能

### 4.1 主要端点

LangServe 为每个部署的链自动创建两个主要端点：

1. **POST /invoke**
   - 功能：执行链的完整调用
   - 请求体：链的输入参数（自动从链的输入模式推导）
   - 响应：链的输出结果
2. **POST /stream**
   - 功能：流式返回链的输出（如果链支持流式输出）
   - 请求体：与 `/invoke` 相同
   - 响应：流式 JSON 数据

### 4.2 输入输出模型

LangServe 会根据链的结构自动生成 Pydantic 模型：

- **输入模型**：基于链的输入变量
- **输出模型**：基于链的输出格式

例如，对于前面的问答链，输入模型为：

python运行

```python
class Input(BaseModel):
    question: str
```



输出模型为：

python运行

```python
class Output(BaseModel):
    text: str
```



### 4.3 自定义输入输出

如果你需要更复杂的输入输出结构，可以使用 `@custom_serve` 装饰器：

python运行

```python
from langserve import custom_serve

@custom_serve
def custom_format_chain(chain):
    # 自定义输入模型
    class CustomInput(BaseModel):
        query: str
        context: Optional[str] = None
    
    # 自定义输出模型
    class CustomOutput(BaseModel):
        answer: str
        sources: List[str]
    
    return chain.with_types(
        input_type=CustomInput,
        output_type=CustomOutput,
    )

# 部署自定义格式的链
add_routes(app, custom_format_chain(chain), path="/custom-qa")
```



### 4.4 部署复杂链

LangServe 可以轻松部署包含多个步骤的复杂链：

python运行

```python
from langchain.chains import SequentialChain

# 定义多个步骤的链
prompt1 = PromptTemplate(
    input_variables=["topic"],
    template="为以下主题生成标题：{topic}"
)
chain1 = LLMChain(llm=llm, prompt=prompt1, output_key="title")

prompt2 = PromptTemplate(
    input_variables=["title"],
    template="为以下标题生成内容：{title}"
)
chain2 = LLMChain(llm=llm, prompt=prompt2, output_key="content")

# 组合链
sequential_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["topic"],
    output_variables=["title", "content"]
)

# 部署复杂链
add_routes(app, sequential_chain, path="/content-generator")
```



## 五、高级用法

### 5.1 添加认证

LangServe 完全兼容 FastAPI 的安全机制：

python运行

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != "your-secret-token":
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return credentials.credentials

# 添加认证依赖
add_routes(app, chain, path="/secure-qa", dependencies=[Depends(verify_token)])
```



### 5.2 自定义路由

如果你需要添加额外的自定义路由：

python运行

```python
from fastapi import APIRouter

# 创建自定义路由
router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

# 将自定义路由添加到应用
app.include_router(router, prefix="/api")

# 部署 LangChain 链
add_routes(app, chain, path="/qa")
```



### 5.3 集成其他 FastAPI 组件

LangServe 应用可以与其他 FastAPI 组件无缝集成：

python运行

```python
# 添加 CORS 支持
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加自定义中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```



## 六、部署与生产化

### 6.1 本地开发

bash

```bash
uvicorn main:app --reload
```



### 6.2 生产部署

推荐使用 Gunicorn + Uvicorn 进行生产部署：

bash

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:8000
```



### 6.3 Docker 部署

创建 Dockerfile：

dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```



构建并运行容器：

bash

```bash
docker build -t langserve-app .
docker run -p 8000:80 langserve-app
```



## 七、常见问题与解决方案

### 7.1 跨域请求问题

如果你在前端应用中调用 LangServe API 时遇到跨域问题，添加 CORS 中间件：

python运行

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 替换为你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```



### 7.2 调试技巧

1. 使用 `--reload` 选项在开发期间启用自动重载
2. 查看 Swagger UI 文档以了解 API 结构
3. 使用日志记录调试信息：

python运行

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 在链中添加日志记录
chain = LLMChain(llm=llm, prompt=prompt)
chain.verbose = True  # 启用详细日志
```



### 7.3 性能优化

1. 使用异步 LLM 提供者（如 OpenAI 的异步 API）
2. 增加工作进程数量：`gunicorn -w 8 -k uvicorn.workers.UvicornWorker main:app`
3. 考虑使用负载均衡器（如 Nginx）进行水平扩展

## 八、总结

LangServe 提供了一种简单而强大的方式来部署 LangChain 应用，使开发者能够专注于构建智能应用，而不必担心复杂的服务端实现。通过自动生成 API 端点和文档，LangServe 大大加速了从开发到生产的过程，是构建语言模型驱动服务的理想选择。

通过本指南，你应该能够：

- 理解 LangServe 的基本概念和优势
- 快速部署简单和复杂的 LangChain 链
- 使用高级功能如认证和自定义路由
- 将服务部署到生产环境

如需更详细的文档，请参考 [LangServe 官方文档](https://langserve.readthedocs.io/)。
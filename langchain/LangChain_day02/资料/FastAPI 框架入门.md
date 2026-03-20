# FastAPI 框架入门教程

## 一、FastAPI 简介

### 1.1 什么是 FastAPI

FastAPI 是一个基于 Python 的现代、快速（高性能）的 Web 框架，用于构建 API。它基于标准的 Python 类型提示，使用 Starlette 和 Pydantic，具有以下特点：

- **快速**：性能接近 Node.js 和 Go（得益于 Starlette 和 Pydantic）。
- **高效开发**：代码自动补全率提高约 200% - 300%。
- **更少的 bug**：减少约 40% 的人为错误。
- **直观**：具有出色的编辑器支持，代码可读性强。
- **简单**：易于使用和学习，降低开发成本。
- **短**：减少代码重复，每个参数声明都有多种用途。
- **健壮**：自动生成交互式文档。
- **基于标准**：基于 API 的相关开放标准（OpenAPI 和 JSON Schema）。

### 1.2 应用场景

FastAPI 适用于各种 Web API 开发场景，特别是：

- 需要高性能的 API 服务。
- 数据模型驱动的应用。
- 需要自动生成文档的 API。
- 前后端分离的项目。
- 微服务架构。

### 1.3 学习前提

- 熟悉 Python 基础知识（变量、数据类型、函数、类等）。
- 了解异步编程概念（async/await）。
- 掌握基本的 HTTP 协议知识。

## 二、环境搭建

### 2.1 安装 Python

确保已安装 Python 3.7 或更高版本。可以从[Python 官方网站](https://www.python.org/)下载并安装。

### 2.2 创建虚拟环境

使用 venv 或 conda 创建虚拟环境，避免包冲突。

bash

```bash
# 使用venv
python -m venv fastapi-env
source fastapi-env/bin/activate  # Linux/Mac
fastapi-env\Scripts\activate  # Windows

# 使用conda
conda create -n fastapi-env python=3.9
conda activate fastapi-env
```



### 2.3 安装 FastAPI 和 Uvicorn

Uvicorn 是一个高性能的 ASGI 服务器，用于运行 FastAPI 应用。

bash

```bash
pip install fastapi uvicorn[standard]
```



## 三、第一个 FastAPI 应用

### 3.1 编写 Hello World 应用

创建一个名为`main.py`的文件，内容如下：

python运行

```python
from fastapi import FastAPI

# 创建FastAPI应用实例
app = FastAPI()

# 定义根路径的GET请求处理函数
@app.get("/")
async def root():
    return {"message": "Hello World"}
```



### 3.2 运行应用

在终端中运行以下命令：

bash

```bash
uvicorn main:app --reload
```

- `main`: 包含 FastAPI 应用的 Python 文件（不包含.py 后缀）。
- `app`: 在 main.py 文件中创建的 FastAPI 应用实例（app = FastAPI ()）。
- `--reload`: 开发模式下的自动重载选项，修改代码后自动重启服务器。

### 3.3 访问 API

打开浏览器或使用工具（如 Postman、curl）访问：

- <http://localhost:8000/>

### 3.4 查看自动生成的文档

FastAPI 自动生成交互式 API 文档：

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## 四、路径操作（路由）

### 4.1 路径参数

python运行

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```



- 路径参数`item_id`的类型被声明为`int`，FastAPI 会自动进行类型转换和验证。

### 4.2 查询参数

python运行

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```



- 查询参数`skip`和`limit`是可选的，默认值分别为 0 和 10。

### 4.3 请求体（POST）

python运行

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```



- 使用 Pydantic 模型定义请求体结构。
- FastAPI 自动进行数据解析、验证和序列化。

### 4.4 路径操作装饰器

- `@app.get()`: 处理 HTTP GET 请求。
- `@app.post()`: 处理 HTTP POST 请求。
- `@app.put()`: 处理 HTTP PUT 请求。
- `@app.delete()`: 处理 HTTP DELETE 请求。
- `@app.options()`: 处理 HTTP OPTIONS 请求。
- `@app.head()`: 处理 HTTP HEAD 请求。
- `@app.patch()`: 处理 HTTP PATCH 请求。
- `@app.trace()`: 处理 HTTP TRACE 请求。

## 五、请求参数和验证

### 5.1 查询参数验证

python运行

```python
from fastapi import Query

@app.get("/items/")
async def read_items(
    q: str = Query(
        None, 
        min_length=3, 
        max_length=50, 
        regex="^fixedquery$"
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```



### 5.2 路径参数验证

python运行

```python
from fastapi import Path

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000),
    q: str = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```



### 5.3 请求体验证

python运行

```python
from pydantic import Field

class Item(BaseModel):
    name: str
    description: str = Field(None, title="The description of the item", max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: float = None
```



## 六、响应处理

### 6.1 响应模型

python运行

```python
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```



### 6.2 响应状态码

python运行

```python
@app.post("/items/", status_code=201)
async def create_item(item: Item):
    return item
```



### 6.3 自定义响应

python运行

```python
from fastapi import Response

@app.get("/items/")
async def read_items():
    return Response(content="Hello World", media_type="text/plain")
```



## 七、依赖注入

### 7.1 简单依赖

python运行

```python
async def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```



### 7.2 类作为依赖

python运行

```python
class CommonQueryParams:
    def __init__(self, q: str = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    return commons
```



### 7.3 路径操作装饰器依赖

python运行

```python
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

@app.get("/items/", dependencies=[Depends(verify_token)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```



## 八、错误处理

### 8.1 HTTP 异常

python运行

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```



### 8.2 自定义异常处理

python运行

```python
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```



## 九、安全与认证

### 9.1 API 密钥认证

python运行

```python
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "1234567890"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/protected/", dependencies=[Depends(get_api_key)])
async def protected_route():
    return {"message": "This is a protected route"}
```



### 9.2 JWT 认证

python运行

```python
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# 配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 数据模型
class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

# 安全工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 模拟数据库
users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31W",
        "disabled": False,
    }
}

# 认证函数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# 生成和验证令牌
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=username)
    if user is None:
        raise credentials_exception
    return user

# 路由
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```



## 十、数据库集成

### 10.1 SQLAlchemy 集成

python运行

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 数据库连接
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 数据模型
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# 创建表
Base.metadata.create_all(bind=engine)

# 依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 路由
@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items
```



### 10.2 MongoDB 集成

python运行

```python
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# MongoDB连接
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["fastapi_db"]

# Pydantic模型
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Item(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# 路由
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    result = await db.items.insert_one(item_dict)
    created_item = await db.items.find_one({"_id": result.inserted_id})
    return created_item

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    return item
```



## 十一、中间件和 CORS

### 11.1 中间件

python运行

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```



### 11.2 CORS

python运行

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```



## 十二、测试

### 12.1 使用 TestClient 测试

python运行

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```



### 12.2 测试依赖

python运行

```python
async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token

app = FastAPI(dependencies=[Depends(get_token_header)])

@app.get("/items/")
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

def test_read_items():
    client = TestClient(app)
    response = client.get("/items/", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == [{"item": "Foo"}, {"item": "Bar"}]
```



## 十三、部署

### 13.1 使用 Uvicorn 独立部署

bash

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```



### 13.2 使用 Gunicorn 和 Uvicorn 部署

bash

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```



### 13.3 Docker 部署

dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

bash

```bash
docker build -t my-fastapi-app .
docker run -d -p 80:80 my-fastapi-app
```



## 十四、高级特性

### 14.1 后台任务

python运行

```python
from fastapi import BackgroundTasks

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```



### 14.2 GraphQL 支持

python运行

```python
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from strawberry.fastapi import GraphQLRouter

# 定义GraphQL类型
import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

# 创建GraphQL模式
schema = strawberry.Schema(query=Query)

# 创建FastAPI应用
app = FastAPI()

# 添加GraphQL路由
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
```



### 14.3 WebSocket 支持

python运行

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```



## 十五、最佳实践

### 15.1 项目结构

plaintext

```plaintext
myproject/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   └── routers/
│       ├── __init__.py
│       ├── user.py
│       └── item.py
└── tests/
    ├── __init__.py
    ├── test_main.py
    ├── test_user.py
    └── test_item.py
```



### 15.2 配置管理

python运行

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

    class Config:
        env_file = ".env"

settings = Settings()
```



### 15.3 日志配置

python运行

```python
import logging
from fastapi import FastAPI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}
```



## 十六、总结

通过本讲义，你已经学习了 FastAPI 的基础知识和高级特性，包括：

- FastAPI 的特点和应用场景
- 环境搭建和第一个应用
- 路径操作和请求参数处理
- 响应处理和依赖注入
- 错误处理和安全认证
- 数据库集成和测试
- 部署和高级特性

FastAPI 凭借其高性能、易用性和丰富的功能，成为 Python Web API 开发的首选框架。希望你能在实际项目中应用这些知识，开发出高效、稳定的 API 服务。
# Vanna PostgreSQL 分析 Demo

这个目录现在包含两个示例：

- `index.py`：保留原来的最小 CLI Demo。
- `backend/` + `frontend/`：前后端分离的复杂 Demo，数据库使用 PostgreSQL。

## 1. 初始化 PostgreSQL

如果你已经在本地 Docker 里启动了 PostgreSQL，可以直接导入 SQL：

```bash
cd /Users/aishawn/code/AIBlog
psql "postgresql://vanna:vanna123@localhost:5432/vanna_demo" -f langchain/VannaAI/backend/db/init/001_schema.sql
psql "postgresql://vanna:vanna123@localhost:5432/vanna_demo" -f langchain/VannaAI/backend/db/init/002_seed_data.sql
```

也可以使用本目录的 Compose 文件启动一个新 PostgreSQL：

```bash
cd /Users/aishawn/code/AIBlog/langchain/VannaAI
docker compose up -d postgres
```

## 2. 启动后端

```bash
cd /Users/aishawn/code/AIBlog/langchain/VannaAI/backend
cp .env.example .env
# 修改 .env 中的 DATABASE_URL 和 DEEPSEEK_API_KEY
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python db/scripts/reset_db.py
uvicorn app.main:app --reload --port 8000
```

后端接口：

- `GET /health`
- `GET /api/schema`
- `POST /api/chat`
- `GET /api/history`

## 3. 启动前端

```bash
cd /Users/aishawn/code/AIBlog/langchain/VannaAI/frontend
cp .env.example .env
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`。

## 4. 可测试的问题

- 各城市 GMV 排名前 5 是多少？
- 按商品品类统计销售额和利润
- 5 月每天的 GMV 趋势是什么？
- 退款率最高的商品品类是什么？
- 不同会员等级的客单价是多少？

## 5. 旧 CLI Demo

```bash
cd /Users/aishawn/code/AIBlog
source .venv/bin/activate
python langchain/VannaAI/index.py
```
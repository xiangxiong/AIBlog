ecommerce-agent/
├── backend/                # FastAPI 后端
│   ├── main.py             # 入口文件
│   ├── agent_engine.py     # LangChain Agent 逻辑
│   ├── knowledge_base.py   # RAG 向量库加载与 CRAG 优化
│   └── data/
│       └── knowledge.json  # 存储商品及售后信息 [cite: 11, 17]
├── frontend/               # React 前端
│   ├── src/
│   │   ├── components/     # 聊天组件
│   │   └── App.js
│   └── package.json
└── docker-compose.yml      # 一键部署配置

运行方法：
1. 启动后端：cd backend && uvicorn main:app --reload
2. 启动前端：cd frontend && npm start

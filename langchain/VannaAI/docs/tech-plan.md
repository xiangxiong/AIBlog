# Vanna PostgreSQL Demo 技术方案

## 目标

构建一个前后端分离的自然语言数据分析 Demo：

- 前端使用 React + Vite。
- 后端使用 FastAPI。
- 数据库使用本地 Docker PostgreSQL。
- Vanna 负责基于业务 Schema 生成 PostgreSQL SQL。
- 后端执行只读 SQL，并返回 SQL、表格结果、图表建议和中文总结。

## 架构

```text
React Frontend
  -> FastAPI Backend
    -> Vanna / OpenAI-compatible LLM
    -> PostgreSQL Business Tables
    -> PostgreSQL App History Tables
```

## 核心模块

- `backend/db/init`：PostgreSQL 初始化 SQL。
- `backend/app/services/schema_service.py`：读取业务表结构，生成 Vanna Prompt 上下文。
- `backend/app/services/vanna_service.py`：调用 Vanna LLM 服务生成 SQL 和总结。
- `backend/app/services/sql_guard.py`：限制只允许 SELECT/WITH。
- `backend/app/services/query_service.py`：执行 PostgreSQL 查询。
- `backend/app/services/history_service.py`：保存会话、消息和查询日志。
- `frontend/src/App.tsx`：分析台主界面。

## 开发顺序

1. 初始化 PostgreSQL 表结构和种子数据。
2. 启动 FastAPI 后端并验证 `/health`。
3. 验证 `/api/schema` 能读取业务表结构。
4. 验证 `/api/chat` 能完成自然语言到 SQL 的闭环。
5. 启动 React 前端进行联调。
6. 根据失败问题补充 Prompt 规则和 few-shot 示例。

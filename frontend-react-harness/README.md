# frontend-react-harness

[![CI 状态](https://github.com/xiangxiong/AIBlog/actions/workflows/frontend-react-harness-ci.yml/badge.svg)](https://github.com/xiangxiong/AIBlog/actions/workflows/frontend-react-harness-ci.yml)

这是一个独立的 React + TypeScript + Vite 前端项目模板。它的目标不只是把页面跑起来，而是把 harness engineering 的工作方式一起沉淀进仓库。

## 项目内置内容

- `AGENTS.md`：给人和智能体看的仓库入口地图
- `docs/`：项目知识库与执行记录系统
- 分层目录结构：降低智能体实现时的结构漂移
- `scripts/check-architecture.mjs`：校验代码导入边界
- `scripts/check-docs.mjs`：校验关键文档是否齐全

## 常用命令

```bash
npm install
npm run dev
npm run lint
npm run test
npm run test:coverage
npm run build
```

## 为什么要这样搭

这个模板把“少依赖临时提示词，多依赖仓库上下文和机械校验”的方式做成了一个最小前端工程骨架，方便后续把更多真实需求交给 AI 稳定执行。

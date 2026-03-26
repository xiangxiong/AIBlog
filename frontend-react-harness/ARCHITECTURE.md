# 架构说明

## 目标

这个项目要尽量对智能体友好。仓库应该通过稳定文件、可预测目录和可执行检查，自解释地告诉协作者“这里是怎么工作的”。

## 代码结构

- `src/app`：应用壳层与整体组装
- `src/domains/<domain>/types`：领域数据契约
- `src/domains/<domain>/service`：纯领域逻辑与内容整理
- `src/domains/<domain>/ui`：面向该领域的 React 组件
- `src/shared`：可复用组件与通用工具

当前已落地的领域包括：

- `home`：项目首页与方法说明
- `auth`：登录流程
- `dashboard`：控制台摘要

## 导入边界

- `src/app` 可以依赖 `src/app` 自身、`src/domains/*/ui` 和 `src/shared/*`
- `src/domains/*/ui` 可以依赖同级的 `service`、`types`，以及 `src/shared/*`
- `src/domains/*/service` 可以依赖同级的 `types`，以及 `src/shared/*`
- `src/domains/*/types` 应保持尽量轻量
- `src/shared/*` 不能反向依赖 `src/app` 或 `src/domains/*`

这些规则由 `scripts/check-architecture.mjs` 自动校验。

## 路由与状态

- 路由编排与访问守卫放在 `src/app`
- 会话存储和通用请求工具放在 `src/shared`
- 领域内的数据获取与整理放在各自的 `service`
- 全局消息提示也放在 `src/shared`，但表单状态仍放在各自页面内部

## 文档原则

凡是智能体会反复用到的内容，都应该进入仓库。不要把产品规则或架构决策只留在聊天记录里。

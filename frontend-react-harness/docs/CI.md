# CI 基线

## 当前流水线

GitHub Actions 会在 `push` 和 `pull_request` 时自动执行：

- `npm ci`
- `npm run lint`
- `npm run test`
- `npm run test:coverage`
- `npm run build`

## 目标

让项目在进入评审前，先自动完成类型检查、守卫检查、测试和构建验证。

## 后续建议

- 增加测试覆盖率上报
- 增加 PR 注释或状态徽章
- 在需要时拆分为更细的前端验证任务

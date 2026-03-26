import type { DashboardSnapshot } from "../types/dashboard";
import { fakeRequest } from "../../../shared/lib/http";

export async function getDashboardSnapshot() {
  const snapshot: DashboardSnapshot = {
    title: "团队控制台",
    subtitle: "这里展示最小业务信息流，后续可以平滑替换为真实接口。",
    metrics: [
      {
        label: "活跃执行计划",
        value: "3 个",
        trend: "较昨日 +1"
      },
      {
        label: "待补文档项",
        value: "2 项",
        trend: "本周下降 40%"
      },
      {
        label: "守卫通过率",
        value: "98%",
        trend: "最近 7 天稳定"
      }
    ],
    todos: [
      {
        title: "补齐 API 错误态",
        detail: "为真实请求封装超时、重试和统一错误提示。"
      },
      {
        title: "接入真实后端",
        detail: "把当前假数据服务替换成 fetch 客户端与环境变量配置。"
      },
      {
        title: "添加测试基线",
        detail: "为路由守卫、登录提交和控制台渲染补充自动化测试。"
      }
    ]
  };

  return fakeRequest(snapshot, 320);
}

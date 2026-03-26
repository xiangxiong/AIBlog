import { useEffect, useState } from "react";
import { getDashboardSnapshot } from "../service/getDashboardSnapshot";
import type { DashboardSnapshot } from "../types/dashboard";
import { useSession } from "../../../shared/lib/session";
import { pushToast } from "../../../shared/lib/uiStore";

export function DashboardPage() {
  const session = useSession();
  const [snapshot, setSnapshot] = useState<DashboardSnapshot | null>(null);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    let cancelled = false;

    getDashboardSnapshot()
      .then((result) => {
        if (!cancelled) {
          setSnapshot(result);
        }
      })
      .catch((error) => {
        if (!cancelled) {
          const message =
            error instanceof Error ? error.message : "控制台数据加载失败，请稍后重试。";
          setLoadError(message);
          pushToast({
            title: "控制台加载失败",
            description: message,
            tone: "error"
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main className="page-shell">
      <section className="hero dashboard-hero">
        <span className="eyebrow">已登录</span>
        <div className="hero-grid">
          <div>
            <h1>{snapshot?.title ?? "载入中..."}</h1>
            <p>
              欢迎回来，{session?.name}。{snapshot?.subtitle ?? "正在准备控制台摘要。"}
            </p>
          </div>
          <div className="hero-panel session-panel">
            <article className="metric-card">
              <span>当前身份</span>
              <strong>{session?.role ?? "-"}</strong>
              <p>{session?.email}</p>
            </article>
          </div>
        </div>
      </section>

      <section className="content-grid">
        {(snapshot?.metrics ?? []).map((metric) => (
          <article className="section-card" key={metric.label}>
            <h2>{metric.label}</h2>
            <p className="metric-value">{metric.value}</p>
            <p>{metric.trend}</p>
          </article>
        ))}
      </section>

      <section className="content-grid content-grid-single">
        <article className="section-card">
          <h2>下一步建议</h2>
          {loadError ? <p className="form-error">{loadError}</p> : null}
          <ul>
            {(snapshot?.todos ?? []).map((todo) => (
              <li key={todo.title}>
                <strong>{todo.title}</strong>
                <div className="todo-detail">{todo.detail}</div>
              </li>
            ))}
          </ul>
        </article>
      </section>
    </main>
  );
}

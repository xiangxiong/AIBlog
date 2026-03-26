import { Link } from "react-router-dom";
import { SectionCard } from "../../../shared/components/SectionCard";
import { getHarnessPlaybook } from "../service/getHarnessPlaybook";

export function HarnessPlaybook() {
  const playbook = getHarnessPlaybook();

  return (
    <main className="page-shell">
      <section className="hero">
        <span className="eyebrow">Agent-first starter</span>
        <div className="hero-grid">
          <div>
            <h1>{playbook.heroTitle}</h1>
            <p>{playbook.heroSummary}</p>
            <div className="hero-actions">
              <Link className="primary-button" to="/login">
                进入登录流
              </Link>
              <Link className="ghost-button" to="/console">
                直接查看控制台
              </Link>
            </div>
          </div>
          <div className="hero-panel">
            {playbook.metrics.map((metric) => (
              <article className="metric-card" key={metric.label}>
                <span>{metric.label}</span>
                <strong>{metric.value}</strong>
                <p>{metric.detail}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="content-grid">
        {playbook.sections.map((section) => (
          <SectionCard
            key={section.title}
            title={section.title}
            summary={section.summary}
            bullets={section.bullets}
          />
        ))}
      </section>

      <p className="footer-note">{playbook.footerNote}</p>
    </main>
  );
}

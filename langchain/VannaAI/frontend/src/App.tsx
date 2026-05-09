import { FormEvent, useEffect, useMemo, useState } from "react";

import { askQuestion, fetchHistory, fetchSchema } from "./api";
import type { ChatResponse, HistoryItem, SchemaResponse } from "./types";

const EXAMPLE_QUESTIONS = [
  "各城市 GMV 排名前 5 是多少？",
  "按商品品类统计销售额和利润",
  "5 月每天的 GMV 趋势是什么？",
  "退款率最高的商品品类是什么？",
];

export default function App() {
  const [question, setQuestion] = useState(EXAMPLE_QUESTIONS[0]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [answer, setAnswer] = useState<ChatResponse | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [schema, setSchema] = useState<SchemaResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void refreshSidebarData();
  }, []);

  async function refreshSidebarData() {
    try {
      const [historyData, schemaData] = await Promise.all([fetchHistory(), fetchSchema()]);
      setHistory(historyData);
      setSchema(schemaData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "加载侧边栏数据失败");
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!question.trim() || loading) {
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await askQuestion(question.trim(), sessionId);
      setAnswer(response);
      setSessionId(response.session_id);
      await refreshSidebarData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "请求失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <aside className="sidebar">
        <h1>Vanna 分析台</h1>
        <p className="muted">React + FastAPI + PostgreSQL 的自然语言数据分析示例。</p>

        <section>
          <h2>历史会话</h2>
          <div className="history-list">
            {history.length === 0 ? (
              <p className="muted">暂无历史记录</p>
            ) : (
              history.map((item) => (
                <button
                  key={item.id}
                  className={item.id === sessionId ? "history-item active" : "history-item"}
                  onClick={() => setSessionId(item.id)}
                >
                  {item.title}
                </button>
              ))
            )}
          </div>
        </section>
      </aside>

      <section className="workspace">
        <form className="question-card" onSubmit={handleSubmit}>
          <label htmlFor="question">输入中文数据问题</label>
          <textarea
            id="question"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            rows={4}
          />
          <div className="examples">
            {EXAMPLE_QUESTIONS.map((example) => (
              <button key={example} type="button" onClick={() => setQuestion(example)}>
                {example}
              </button>
            ))}
          </div>
          <button className="primary" disabled={loading} type="submit">
            {loading ? "分析中..." : "开始分析"}
          </button>
        </form>

        {error ? <div className="error">{error}</div> : null}
        {answer ? <AnswerPanel answer={answer} /> : <EmptyState />}
      </section>

      <aside className="schema-panel">
        <h2>业务 Schema</h2>
        {schema ? <SchemaView schema={schema} /> : <p className="muted">正在加载表结构...</p>}
      </aside>
    </main>
  );
}

function EmptyState() {
  return (
    <section className="empty">
      <h2>准备好提问了</h2>
      <p>后端会让 Vanna 基于 PostgreSQL 表结构生成 SQL，并返回查询结果、图表建议和中文总结。</p>
    </section>
  );
}

function AnswerPanel({ answer }: { answer: ChatResponse }) {
  return (
    <section className="answer-grid">
      {answer.error ? <div className="error">{answer.error}</div> : null}

      <article className="card">
        <div className="card-header">
          <h2>分析总结</h2>
          <span>{answer.execution_ms} ms</span>
        </div>
        <p>{answer.summary || "暂无总结，查看 SQL 和表格结果。"}</p>
      </article>

      {answer.sql ? (
        <article className="card">
          <h2>生成 SQL</h2>
          <pre>{answer.sql}</pre>
        </article>
      ) : null}

      {answer.chart ? (
        <article className="card">
          <h2>图表预览</h2>
          <SimpleChart answer={answer} />
          <p className="muted">{answer.chart.reason}</p>
        </article>
      ) : null}

      <article className="card">
        <div className="card-header">
          <h2>查询结果</h2>
          <span>{answer.row_count} 行</span>
        </div>
        <ResultTable columns={answer.columns} rows={answer.rows} />
      </article>
    </section>
  );
}

function ResultTable({ columns, rows }: { columns: string[]; rows: unknown[][] }) {
  if (columns.length === 0) {
    return <p className="muted">暂无结果</p>;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={`${rowIndex}-${row.join("-")}`}>
              {row.map((cell, cellIndex) => (
                <td key={`${rowIndex}-${cellIndex}`}>{String(cell ?? "")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SimpleChart({ answer }: { answer: ChatResponse }) {
  const chartData = useMemo(() => {
    if (!answer.chart?.x || !answer.chart?.y) {
      return [];
    }
    const xIndex = answer.columns.indexOf(answer.chart.x);
    const yIndex = answer.columns.indexOf(answer.chart.y);
    if (xIndex < 0 || yIndex < 0) {
      return [];
    }
    return answer.rows
      .map((row) => ({
        label: String(row[xIndex]),
        value: Number(row[yIndex]),
      }))
      .filter((item) => Number.isFinite(item.value));
  }, [answer]);

  if (chartData.length === 0) {
    return <p className="muted">当前结果不适合绘制图表。</p>;
  }

  const maxValue = Math.max(...chartData.map((item) => item.value), 1);
  return (
    <div className="chart">
      {chartData.map((item) => (
        <div className="bar-row" key={item.label}>
          <span>{item.label}</span>
          <div className="bar-track">
            <div className="bar" style={{ width: `${(item.value / maxValue) * 100}%` }} />
          </div>
          <strong>{item.value.toLocaleString()}</strong>
        </div>
      ))}
    </div>
  );
}

function SchemaView({ schema }: { schema: SchemaResponse }) {
  return (
    <div className="schema-list">
      {schema.tables.map((table) => (
        <section key={table} className="schema-table">
          <h3>{table}</h3>
          {schema.columns
            .filter((column) => column.table_name === table)
            .map((column) => (
              <div key={`${table}-${column.column_name}`} className="schema-column">
                <span>{column.column_name}</span>
                <code>{column.data_type}</code>
              </div>
            ))}
        </section>
      ))}
    </div>
  );
}

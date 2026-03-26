import { startTransition, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { getDemoCredentials, login } from "../service/authService";
import {
  validateLoginForm,
  type LoginFieldErrors
} from "../service/validateLoginForm";
import { pushToast } from "../../../shared/lib/uiStore";

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const from = readFromState(location.state);
  const demo = getDemoCredentials();

  const [form, setForm] = useState({
    email: demo.email,
    password: demo.password
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState<LoginFieldErrors>({});

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    const nextFieldErrors = validateLoginForm(form);
    setFieldErrors(nextFieldErrors);

    if (Object.keys(nextFieldErrors).length > 0) {
      pushToast({
        title: "表单未通过校验",
        description: "请先修正邮箱和密码，再继续登录。",
        tone: "error"
      });
      return;
    }

    setIsSubmitting(true);

    try {
      await login(form);
      pushToast({
        title: "登录成功",
        description: "欢迎进入控制台，接下来可以继续扩展真实业务流程。",
        tone: "success"
      });
      startTransition(() => {
        navigate(from, { replace: true });
      });
    } catch (submissionError) {
      const message =
        submissionError instanceof Error ? submissionError.message : "登录失败";
      setError(message);
      pushToast({
        title: "登录失败",
        description: message,
        tone: "error"
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="content-grid content-grid-login">
        <article className="section-card login-copy">
          <span className="eyebrow">业务演示入口</span>
          <h2>登录后进入控制台</h2>
          <p>
            这里是一个最小业务流示例：通过路由、会话和 API
            抽象，把“静态展示模板”升级成“可以承载真实业务”的前端骨架。
          </p>
          <ul>
            <li>路由层负责页面编排和访问控制</li>
            <li>领域服务层负责登录与数据获取</li>
            <li>共享层负责会话状态和请求模拟</li>
          </ul>
        </article>

        <article className="section-card login-panel">
          <div className="credential-box">
            <strong>演示账号</strong>
            <span>{demo.email}</span>
            <span>{demo.password}</span>
          </div>

          <form className="login-form" onSubmit={handleSubmit}>
            <label>
              邮箱
              <input
                autoComplete="email"
                name="email"
                onChange={(event) => {
                  const value = event.target.value;
                  setForm((current) => ({ ...current, email: value }));
                  setFieldErrors((current) => ({ ...current, email: undefined }));
                }}
                type="email"
                value={form.email}
              />
              {fieldErrors.email ? <span className="field-error">{fieldErrors.email}</span> : null}
            </label>
            <label>
              密码
              <input
                autoComplete="current-password"
                name="password"
                onChange={(event) => {
                  const value = event.target.value;
                  setForm((current) => ({ ...current, password: value }));
                  setFieldErrors((current) => ({ ...current, password: undefined }));
                }}
                type="password"
                value={form.password}
              />
              {fieldErrors.password ? (
                <span className="field-error">{fieldErrors.password}</span>
              ) : null}
            </label>

            {error ? <p className="form-error">{error}</p> : null}

            <button className="primary-button" disabled={isSubmitting} type="submit">
              {isSubmitting ? "登录中..." : "进入控制台"}
            </button>
          </form>
        </article>
      </section>
    </main>
  );
}

function readFromState(state: unknown) {
  if (typeof state === "object" && state !== null && "from" in state) {
    const from = (state as { from?: unknown }).from;
    if (typeof from === "string" && from.length > 0) {
      return from;
    }
  }

  return "/console";
}

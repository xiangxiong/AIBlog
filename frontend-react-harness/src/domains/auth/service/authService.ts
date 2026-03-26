import type { LoginInput, SessionUser } from "../types/auth";
import { fakeRequest } from "../../../shared/lib/http";
import { setSession } from "../../../shared/lib/session";

const DEMO_ACCOUNT = {
  email: "demo@aiblog.dev",
  password: "codex123",
  role: "产品管理员"
};

export async function login(input: LoginInput) {
  const normalizedEmail = input.email.trim().toLowerCase();
  const normalizedPassword = input.password.trim();

  if (
    normalizedEmail !== DEMO_ACCOUNT.email ||
    normalizedPassword !== DEMO_ACCOUNT.password
  ) {
    await fakeRequest(null, 450);
    throw new Error("账号或密码错误，请使用演示账号登录。");
  }

  const session: SessionUser = {
    email: DEMO_ACCOUNT.email,
    name: "AIBlog Demo",
    role: DEMO_ACCOUNT.role
  };

  const result = await fakeRequest(session, 550);
  setSession(result);
  return result;
}

export function getDemoCredentials() {
  return {
    email: DEMO_ACCOUNT.email,
    password: DEMO_ACCOUNT.password
  };
}

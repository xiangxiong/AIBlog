import type { LoginInput } from "../types/auth";

export type LoginFieldErrors = {
  email?: string;
  password?: string;
};

export function validateLoginForm(input: LoginInput) {
  const errors: LoginFieldErrors = {};
  const email = input.email.trim();
  const password = input.password.trim();

  if (!email) {
    errors.email = "请输入邮箱地址。";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.email = "请输入有效的邮箱格式。";
  }

  if (!password) {
    errors.password = "请输入密码。";
  } else if (password.length < 6) {
    errors.password = "密码长度至少为 6 位。";
  }

  return errors;
}

import { describe, expect, it } from "vitest";
import { validateLoginForm } from "../../src/domains/auth/service/validateLoginForm";

describe("validateLoginForm", () => {
  it("在表单为空时返回必填错误", () => {
    expect(validateLoginForm({ email: "", password: "" })).toEqual({
      email: "请输入邮箱地址。",
      password: "请输入密码。"
    });
  });

  it("在邮箱格式错误和密码过短时返回对应错误", () => {
    expect(validateLoginForm({ email: "hello", password: "123" })).toEqual({
      email: "请输入有效的邮箱格式。",
      password: "密码长度至少为 6 位。"
    });
  });

  it("在输入有效时返回空错误对象", () => {
    expect(
      validateLoginForm({
        email: "demo@aiblog.dev",
        password: "codex123"
      })
    ).toEqual({});
  });
});

import { afterEach, describe, expect, it, vi } from "vitest";
import { login } from "../../src/domains/auth/service/authService";
import { clearSession, getSession } from "../../src/shared/lib/session";

describe("authService", () => {
  afterEach(() => {
    vi.useRealTimers();
    clearSession();
  });

  it("使用演示账号时写入会话", async () => {
    vi.useFakeTimers();

    const loginPromise = login({
      email: "demo@aiblog.dev",
      password: "codex123"
    });
    const assertion = expect(loginPromise).resolves.toMatchObject({
      email: "demo@aiblog.dev",
      role: "产品管理员"
    });

    await vi.advanceTimersByTimeAsync(600);
    await assertion;
    expect(getSession()).toMatchObject({
      email: "demo@aiblog.dev"
    });
  });

  it("账号错误时返回失败且不写入会话", async () => {
    vi.useFakeTimers();

    const loginPromise = login({
      email: "wrong@aiblog.dev",
      password: "bad-pass"
    });
    const assertion = expect(loginPromise).rejects.toThrow(
      "账号或密码错误，请使用演示账号登录。"
    );

    await vi.advanceTimersByTimeAsync(500);
    await assertion;
    expect(getSession()).toBeNull();
  });
});

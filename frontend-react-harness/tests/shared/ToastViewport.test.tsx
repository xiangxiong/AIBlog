import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { ToastViewport } from "../../src/shared/components/ToastViewport";
import { clearToasts, pushToast } from "../../src/shared/lib/uiStore";

describe("ToastViewport", () => {
  it("可以展示并手动关闭通知", async () => {
    const user = userEvent.setup();
    render(<ToastViewport />);

    act(() => {
      pushToast({
        title: "保存成功",
        description: "内容已经同步到本地。",
        tone: "success"
      });
    });

    expect(screen.getByText("保存成功")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "关闭通知" }));
    expect(screen.queryByText("保存成功")).not.toBeInTheDocument();
  });

  it("会在定时器到期后自动移除通知", async () => {
    vi.useFakeTimers();
    render(<ToastViewport />);

    act(() => {
      pushToast({
        title: "自动关闭",
        description: "三秒多后自动消失。",
        tone: "info"
      });
    });

    expect(screen.getByText("自动关闭")).toBeInTheDocument();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(3300);
    });

    expect(screen.queryByText("自动关闭")).not.toBeInTheDocument();
    clearToasts();
    vi.useRealTimers();
  });
});

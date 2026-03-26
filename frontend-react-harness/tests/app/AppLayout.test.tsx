import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { AppLayout } from "../../src/app/AppLayout";
import { clearSession, setSession } from "../../src/shared/lib/session";

describe("AppLayout", () => {
  it("未登录时显示登录入口", async () => {
    clearSession();

    const router = createMemoryRouter(
      [
        {
          path: "/",
          element: <AppLayout />,
          children: [
            {
              index: true,
              element: <div>首页内容</div>
            }
          ]
        }
      ],
      { initialEntries: ["/"] }
    );

    render(<RouterProvider router={router} />);

    expect(screen.getByRole("link", { name: "登录" })).toBeInTheDocument();
  });

  it("登录后可以退出并跳回首页，同时展示提示", async () => {
    const user = userEvent.setup();
    setSession({
      email: "demo@aiblog.dev",
      name: "AIBlog Demo",
      role: "产品管理员"
    });

    const router = createMemoryRouter(
      [
        {
          path: "/",
          element: <AppLayout />,
          children: [
            {
              index: true,
              element: <div>首页内容</div>
            },
            {
              path: "console",
              element: <div>控制台内容</div>
            }
          ]
        }
      ],
      { initialEntries: ["/console"] }
    );

    render(<RouterProvider router={router} />);

    expect(screen.getByRole("button", { name: "退出登录" })).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "退出登录" }));

    expect(await screen.findByText("首页内容")).toBeInTheDocument();
    expect(screen.getByText("已退出登录")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "登录" })).toBeInTheDocument();
  });
});

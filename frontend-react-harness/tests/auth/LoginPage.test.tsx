import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { LoginPage } from "../../src/domains/auth/ui/LoginPage";
import { ToastViewport } from "../../src/shared/components/ToastViewport";
import { getSession } from "../../src/shared/lib/session";

describe("LoginPage", () => {
  it("表单为空时展示字段错误", async () => {
    const user = userEvent.setup();
    const router = createMemoryRouter(
      [
        {
          path: "/",
          element: (
            <>
              <ToastViewport />
              <LoginPage />
            </>
          )
        },
        {
          path: "/console",
          element: <div>控制台页面</div>
        }
      ],
      { initialEntries: ["/"] }
    );

    render(<RouterProvider router={router} />);

    await user.clear(screen.getByRole("textbox", { name: "邮箱" }));
    await user.clear(screen.getByLabelText("密码"));
    await user.click(screen.getByRole("button", { name: "进入控制台" }));

    expect(screen.getByText("请输入邮箱地址。")).toBeInTheDocument();
    expect(screen.getByText("请输入密码。")).toBeInTheDocument();
    expect(screen.getByText("表单未通过校验")).toBeInTheDocument();
  });

  it("使用演示账号登录后跳转到控制台", async () => {
    const user = userEvent.setup();
    const router = createMemoryRouter(
      [
        {
          path: "/",
          element: (
            <>
              <ToastViewport />
              <LoginPage />
            </>
          )
        },
        {
          path: "/console",
          element: <div>控制台页面</div>
        }
      ],
      { initialEntries: ["/"] }
    );

    render(<RouterProvider router={router} />);

    await user.click(screen.getByRole("button", { name: "进入控制台" }));

    expect(await screen.findByText("控制台页面")).toBeInTheDocument();
    expect(getSession()).toMatchObject({
      email: "demo@aiblog.dev"
    });
  });
});

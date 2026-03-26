import { render, screen } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { RequireAuth } from "../../src/app/RequireAuth";
import { clearSession, setSession } from "../../src/shared/lib/session";

describe("RequireAuth", () => {
  it("未登录时跳转到登录页", async () => {
    clearSession();

    const router = createMemoryRouter(
      [
        {
          path: "/",
          children: [
            {
              path: "login",
              element: <div>登录页</div>
            },
            {
              element: <RequireAuth />,
              children: [
                {
                  path: "console",
                  element: <div>控制台</div>
                }
              ]
            }
          ]
        }
      ],
      {
        initialEntries: ["/console"]
      }
    );

    render(<RouterProvider router={router} />);

    expect(await screen.findByText("登录页")).toBeInTheDocument();
  });

  it("已登录时允许进入受保护页面", async () => {
    setSession({
      email: "demo@aiblog.dev",
      name: "AIBlog Demo",
      role: "产品管理员"
    });

    const router = createMemoryRouter(
      [
        {
          path: "/",
          children: [
            {
              path: "login",
              element: <div>登录页</div>
            },
            {
              element: <RequireAuth />,
              children: [
                {
                  path: "console",
                  element: <div>控制台</div>
                }
              ]
            }
          ]
        }
      ],
      {
        initialEntries: ["/console"]
      }
    );

    render(<RouterProvider router={router} />);

    expect(await screen.findByText("控制台")).toBeInTheDocument();
  });
});

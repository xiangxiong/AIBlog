import { createBrowserRouter } from "react-router-dom";
import { LoginPage } from "../domains/auth/ui/LoginPage";
import { DashboardPage } from "../domains/dashboard/ui/DashboardPage";
import { HarnessPlaybook } from "../domains/home/ui/HarnessPlaybook";
import { AppLayout } from "./AppLayout";
import { RequireAuth } from "./RequireAuth";

function NotFoundPage() {
  return (
    <main className="page-shell">
      <section className="content-grid content-grid-single">
        <article className="section-card">
          <h2>页面不存在</h2>
          <p>你访问的页面没有找到，请从首页或控制台重新进入。</p>
        </article>
      </section>
    </main>
  );
}

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <HarnessPlaybook />
      },
      {
        path: "login",
        element: <LoginPage />
      },
      {
        element: <RequireAuth />,
        children: [
          {
            path: "console",
            element: <DashboardPage />
          }
        ]
      },
      {
        path: "*",
        element: <NotFoundPage />
      }
    ]
  }
]);

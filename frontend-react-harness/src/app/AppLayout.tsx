import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { clearSession, useSession } from "../shared/lib/session";
import { pushToast } from "../shared/lib/uiStore";
import { ToastViewport } from "../shared/components/ToastViewport";

export function AppLayout() {
  const location = useLocation();
  const navigate = useNavigate();
  const session = useSession();

  function handleLogout() {
    clearSession();
    pushToast({
      title: "已退出登录",
      description: "当前会话已经清除，你可以重新登录或返回首页。",
      tone: "info"
    });
    navigate("/");
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-block">
          <span className="brand-kicker">AIBlog Frontend</span>
          <strong>Harness 驱动的业务前端骨架</strong>
        </div>
        <nav className="topnav" aria-label="主导航">
          <NavLink className={getNavClassName} to="/">
            首页
          </NavLink>
          <NavLink className={getNavClassName} to="/console">
            控制台
          </NavLink>
          {session ? (
            <button className="ghost-button" onClick={handleLogout} type="button">
              退出登录
            </button>
          ) : (
            <NavLink
              className={getNavClassName}
              state={{ from: location.pathname }}
              to="/login"
            >
              登录
            </NavLink>
          )}
        </nav>
      </header>
      <ToastViewport />
      <Outlet />
    </div>
  );
}

function getNavClassName({ isActive }: { isActive: boolean }) {
  return isActive ? "nav-link nav-link-active" : "nav-link";
}

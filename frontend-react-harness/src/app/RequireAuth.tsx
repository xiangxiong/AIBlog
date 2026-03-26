import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useSession } from "../shared/lib/session";

export function RequireAuth() {
  const session = useSession();
  const location = useLocation();

  if (!session) {
    return <Navigate replace state={{ from: location.pathname }} to="/login" />;
  }

  return <Outlet />;
}

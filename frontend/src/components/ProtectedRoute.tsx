import { Navigate, Outlet } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { useEffect, useState } from 'react';
import type { RootState } from '../store';
import { DashboardLayout } from './layout/DashboardLayout';
import type { Role } from '../store/authSlice';
import { setUser, logout } from '../store/authSlice';
import { api } from '../lib/api';

interface ProtectedRouteProps {
  allowedRoles?: Role[];
  standalone?: boolean;
}

export function ProtectedRoute({ allowedRoles, standalone = false }: ProtectedRouteProps) {
  const { isAuthenticated, user, token } = useSelector((state: RootState) => state.auth);
  const dispatch = useDispatch();
  const [isInitializing, setIsInitializing] = useState(!user && isAuthenticated);

  useEffect(() => {
    if (isAuthenticated && !user && token) {
      api.get('/accounts/me/')
        .then(res => {
          dispatch(setUser(res.data));
          setIsInitializing(false);
        })
        .catch(() => {
          dispatch(logout());
          setIsInitializing(false);
        });
    } else {
      setIsInitializing(false);
    }
  }, [isAuthenticated, user, token, dispatch]);

  if (isInitializing) {
    if (standalone) {
      return (
        <div className="flex min-h-dvh items-center justify-center bg-slate-950">
          <div className="h-10 w-10 animate-spin rounded-full border-2 border-white/20 border-t-emerald-400" />
        </div>
      );
    }
    return (
      <div className="flex h-screen items-center justify-center bg-slate-900">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && (!user?.role || !allowedRoles.includes(user.role))) {
    // Redirect unauthorized users to their safest default dashboard
    // or just the generic home
    return <Navigate to="/" replace />;
  }

  if (standalone) return <Outlet />;

  return (
    <DashboardLayout>
      <Outlet />
    </DashboardLayout>
  );
}

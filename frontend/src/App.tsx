import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Login } from './pages/Login';
import { useSelector } from 'react-redux';
import type { RootState } from './store';

const ManagerDashboard = lazy(() => import('./pages/ManagerDashboard').then((module) => ({ default: module.ManagerDashboard })));
const HROfficerDashboard = lazy(() => import('./pages/HROfficerDashboard').then((module) => ({ default: module.HROfficerDashboard })));
const CEODashboard = lazy(() => import('./pages/CEODashboard'));
const StaffManagement = lazy(() => import('./pages/StaffManagement').then((module) => ({ default: module.StaffManagement })));
const AttendanceDashboard = lazy(() => import('./pages/AttendanceDashboard').then((module) => ({ default: module.AttendanceDashboard })));
const LeaveDashboard = lazy(() => import('./pages/LeaveDashboard').then((module) => ({ default: module.LeaveDashboard })));
const ReportsPage = lazy(() => import('./pages/ReportsPage').then((module) => ({ default: module.ReportsPage })));
const RecruitmentPage = lazy(() => import('./pages/RecruitmentPage'));
const KioskMode = lazy(() => import('./pages/KioskMode').then((module) => ({ default: module.KioskMode })));
const ReceptionistDashboard = lazy(() => import('./pages/ReceptionistDashboard').then((module) => ({ default: module.ReceptionistDashboard })));
const SettingsPage = lazy(() => import('./pages/SettingsPage').then((module) => ({ default: module.SettingsPage })));
const NuruMobileApp = lazy(() => import('./mobile/NuruMobileApp'));

function PageLoader() {
  return (
    <div className="flex min-h-[50vh] items-center justify-center">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600" />
    </div>
  );
}

// A smart redirect component that sends the user to their appropriate dashboard
function DashboardHome() {
  const { user } = useSelector((state: RootState) => state.auth);

  if (user?.role === 'super_admin' || user?.role === 'director') return <Navigate to="/ceo" replace />;
  if (user?.role === 'hr_officer') return <Navigate to="/hr" replace />;
  if (user?.role === 'manager') return <Navigate to="/manager" replace />;
  if (user?.role === 'receptionist') return <Navigate to="/reception" replace />;

  // Default for standard employees
  return <Navigate to="/app" replace />;
}

function App() {
  return (
    <Router>
      <Suspense fallback={<PageLoader />}>
        <Routes>
        {/* Public Route */}
        <Route path="/login" element={<Login />} />
        <Route path="/mobile" element={<Navigate to="/app" replace />} />

        {/* Protected Routes (Wrapped in DashboardLayout via ProtectedRoute) */}

        {/* Smart Home Redirect */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<DashboardHome />} />
        </Route>

        {/* Employee web app — standalone so it mirrors the APK rather than the admin portal. */}
        <Route element={<ProtectedRoute standalone />}>
          <Route path="/app" element={<NuruMobileApp />} />
        </Route>

        {/* Common Routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/attendance" element={<AttendanceDashboard />} />
          <Route path="/leave" element={<LeaveDashboard />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        {/* Manager & Above */}
        <Route element={<ProtectedRoute allowedRoles={['manager', 'director', 'super_admin']} />}>
          <Route path="/manager" element={<ManagerDashboard />} />
        </Route>

        {/* HR & Above */}
        <Route element={<ProtectedRoute allowedRoles={['hr_officer', 'super_admin']} />}>
          <Route path="/hr" element={<HROfficerDashboard />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={['manager', 'director', 'super_admin', 'hr_officer']} />}>
          <Route path="/staff" element={<StaffManagement />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/recruitment" element={<RecruitmentPage />} />
        </Route>

        {/* Executives & Super Admin */}
        <Route element={<ProtectedRoute allowedRoles={['director', 'super_admin']} />}>
          <Route path="/ceo" element={<CEODashboard />} />
        </Route>

        {/* Receptionist */}
        <Route element={<ProtectedRoute allowedRoles={['receptionist', 'super_admin', 'hr_officer', 'manager', 'director']} />}>
          <Route path="/reception" element={<ReceptionistDashboard />} />
        </Route>

        {/* Kiosk Mode (Needs to be protected but standalone UI) */}
        <Route element={<ProtectedRoute allowedRoles={['director', 'super_admin', 'hr_officer', 'manager', 'receptionist']} />}>
          <Route path="/kiosk" element={<KioskMode />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;

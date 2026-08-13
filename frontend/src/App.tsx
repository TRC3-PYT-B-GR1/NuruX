import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from './components/layout/DashboardLayout';
import { ManagerDashboard } from './pages/ManagerDashboard';
import { HROfficerDashboard } from './pages/HROfficerDashboard';

function App() {
  return (
    <Router>
      <DashboardLayout>
        <Routes>
          <Route path="/" element={<ManagerDashboard />} />
          <Route path="/hr" element={<HROfficerDashboard />} />
          {/* Placeholder for other routes */}
          <Route path="/team" element={<div>My Team Page</div>} />
          <Route path="/attendance" element={<div>Attendance Page</div>} />
          <Route path="/leave" element={<div>Leave Page</div>} />
          <Route path="/reports" element={<div>Reports Page</div>} />
          <Route path="/settings" element={<div>Settings Page</div>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </DashboardLayout>
    </Router>
  );
}

export default App;

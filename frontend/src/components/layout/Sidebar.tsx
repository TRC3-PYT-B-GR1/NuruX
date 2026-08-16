import { NavLink, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Sun, LayoutDashboard, Users, Clock,
  Calendar, FileText, Settings, HelpCircle, LogOut, PanelLeftClose, PanelLeftOpen
} from 'lucide-react';
import { cn } from '../../lib/utils';
import type { RootState } from '../../store';
import { logout } from '../../store/authSlice';
import type { Role } from '../../store/authSlice';
import { api } from '../../lib/api';

interface NavItem {
  name: string;
  icon: React.ElementType;
  path: string;
  roles: Role[];
}

const navItems: NavItem[] = [
  { name: 'CEO Dashboard', icon: LayoutDashboard, path: '/ceo', roles: ['super_admin', 'director'] },
  { name: 'Manager Dashboard', icon: LayoutDashboard, path: '/manager', roles: ['super_admin', 'director', 'manager'] },
  { name: 'HR Dashboard', icon: Users, path: '/hr', roles: ['super_admin', 'hr_officer'] },
  { name: 'Staff Directory', icon: Users, path: '/staff', roles: ['super_admin', 'director', 'manager', 'hr_officer'] },
  { name: 'Attendance', icon: Clock, path: '/attendance', roles: ['super_admin', 'director', 'manager', 'hr_officer', 'payroll_officer', 'employee'] },
  { name: 'Leave', icon: Calendar, path: '/leave', roles: ['super_admin', 'director', 'manager', 'hr_officer', 'payroll_officer', 'employee'] },
  { name: 'Reception', icon: Clock, path: '/reception', roles: ['super_admin', 'director', 'manager', 'hr_officer', 'receptionist'] },
  { name: 'Reports', icon: FileText, path: '/reports', roles: ['super_admin', 'director', 'hr_officer', 'manager'] },
  { name: 'Settings', icon: Settings, path: '/settings', roles: ['super_admin', 'director', 'manager', 'hr_officer', 'payroll_officer', 'employee', 'receptionist'] },
];

export function Sidebar({ isCollapsed = false, toggleCollapse }: { isCollapsed?: boolean, toggleCollapse?: () => void }) {
  const { user } = useSelector((state: RootState) => state.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = async () => {
    const refresh = localStorage.getItem('nuru_refresh_token');
    try {
      if (refresh) await api.post('/accounts/logout/', { refresh });
    } finally {
      dispatch(logout());
      navigate('/login');
    }
  };

  const visibleNavItems = navItems.filter(item => user?.role && item.roles.includes(user.role));

  return (
    <aside className={cn(
      "bg-slate-900 text-slate-300 h-screen flex flex-col fixed left-0 top-0 border-r border-slate-800 z-20 transition-all duration-300",
      isCollapsed ? "w-20" : "w-64"
    )}>
      {/* Logo Area */}
      <div className={cn("h-16 flex items-center border-b border-slate-800", isCollapsed ? "justify-center px-2" : "px-6 justify-between")}>
        <div className="flex items-center">
          <Sun className={cn("text-yellow-500 flex-shrink-0", isCollapsed ? "h-8 w-8" : "h-6 w-6 mr-2")} />
          {!isCollapsed && <span className="text-xl font-bold text-white tracking-wide">NuruX</span>}
        </div>
        {!isCollapsed && toggleCollapse && (
          <button onClick={toggleCollapse} className="text-slate-400 hover:text-white transition-colors">
            <PanelLeftClose className="h-5 w-5" />
          </button>
        )}
      </div>

      {isCollapsed && toggleCollapse && (
        <div className="flex justify-center mt-4">
          <button onClick={toggleCollapse} className="text-slate-400 hover:text-white transition-colors">
            <PanelLeftOpen className="h-5 w-5" />
          </button>
        </div>
      )}

      {/* User Info */}
      {!isCollapsed && (
        <div className="px-6 py-4 border-b border-slate-800">
          <p className="text-sm font-medium text-white truncate">{user?.email}</p>
          <p className="text-xs text-slate-400 capitalize">{user?.role?.replace('_', ' ')}</p>
        </div>
      )}

      {/* Navigation */}
      <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
        {visibleNavItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            title={isCollapsed ? item.name : undefined}
            className={({ isActive }) =>
              cn(
                "flex items-center rounded-md text-sm font-medium transition-colors group",
                isCollapsed ? "justify-center py-3" : "px-3 py-2.5",
                isActive
                  ? "bg-blue-600 text-white shadow-md shadow-blue-900/20"
                  : "hover:bg-slate-800 hover:text-white"
              )
            }
          >
            <item.icon className={cn("flex-shrink-0", isCollapsed ? "h-6 w-6" : "h-5 w-5 mr-3")} />
            {!isCollapsed && <span>{item.name}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Footer / Help */}
      <div className={cn("p-4 border-t border-slate-800 space-y-2", isCollapsed ? "px-2" : "")}>
        <button type="button" onClick={() => navigate('/settings')} title={isCollapsed ? "Help & Support" : undefined} className={cn("w-full flex items-center text-sm font-medium text-slate-400 hover:text-white transition-colors rounded-md hover:bg-slate-800", isCollapsed ? "justify-center py-3" : "px-3 py-2")}>
          <HelpCircle className={cn("flex-shrink-0", isCollapsed ? "h-6 w-6" : "h-5 w-5 mr-3")} />
          {!isCollapsed && <span>Help & Support</span>}
        </button>
        <button
          onClick={handleLogout}
          title={isCollapsed ? "Log Out" : undefined}
          className={cn("w-full flex items-center text-sm font-medium text-red-400 hover:text-red-300 transition-colors rounded-md hover:bg-slate-800", isCollapsed ? "justify-center py-3" : "px-3 py-2")}
        >
          <LogOut className={cn("flex-shrink-0", isCollapsed ? "h-6 w-6" : "h-5 w-5 mr-3")} />
          {!isCollapsed && <span>Log Out</span>}
        </button>
      </div>
    </aside>
  );
}

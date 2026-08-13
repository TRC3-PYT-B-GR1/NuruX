import { NavLink } from 'react-router-dom';
import { 
  Sun, LayoutDashboard, Users, Clock, 
  Calendar, FileText, Settings, HelpCircle
} from 'lucide-react';
import { cn } from '../../lib/utils';

const navItems = [
  { name: 'Manager Dashboard', icon: LayoutDashboard, path: '/manager' },
  { name: 'HR Dashboard', icon: Users, path: '/hr' },
  { name: 'Attendance', icon: Clock, path: '/attendance' },
  { name: 'Leave', icon: Calendar, path: '/leave' },
  { name: 'Reports', icon: FileText, path: '/reports' },
  { name: 'Settings', icon: Settings, path: '/settings' },
];

export function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-slate-300 h-screen flex flex-col fixed left-0 top-0 border-r border-slate-800 z-20">
      {/* Logo Area */}
      <div className="h-16 flex items-center px-6 border-b border-slate-800">
        <Sun className="h-6 w-6 text-yellow-500 mr-2" />
        <span className="text-xl font-bold text-white tracking-wide">NuruX</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              cn(
                "flex items-center px-3 py-2.5 rounded-md text-sm font-medium transition-colors group",
                isActive 
                  ? "bg-blue-600 text-white" 
                  : "hover:bg-slate-800 hover:text-white"
              )
            }
          >
            <item.icon className="h-5 w-5 mr-3 flex-shrink-0" />
            {item.name}
          </NavLink>
        ))}
      </nav>

      {/* Footer / Help */}
      <div className="p-4 border-t border-slate-800">
        <a href="#" className="flex items-center px-3 py-2 text-sm font-medium text-slate-400 hover:text-white transition-colors rounded-md hover:bg-slate-800">
          <HelpCircle className="h-5 w-5 mr-3" />
          Help & Support
        </a>
      </div>
    </aside>
  );
}

import { Search, Bell, ChevronDown, LogOut, Settings } from 'lucide-react';
import { useSelector, useDispatch } from 'react-redux';
import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import type { RootState } from '../../store';
import { logout } from '../../store/authSlice';
import { api } from '../../lib/api';

export function TopBar() {
  const { user } = useSelector((state: RootState) => state.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const notificationRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
      if (notificationRef.current && !notificationRef.current.contains(event.target as Node)) {
        setIsNotificationOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = async () => {
    const refresh = localStorage.getItem('nuru_refresh_token');
    try {
      if (refresh) await api.post('/accounts/logout/', { refresh });
    } finally {
      dispatch(logout());
      navigate('/login');
    }
  };

  const displayName = user?.username || 'User';
  const avatarUrl = `https://ui-avatars.com/api/?name=${displayName}&background=random`;

  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
      {/* Search */}
      <div className="flex-1 max-w-md">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-slate-400" />
          </div>
          <input
            type="text"
            className="block w-full pl-10 pr-3 py-2 border border-slate-200 rounded-md leading-5 bg-slate-50 placeholder-slate-400 focus:outline-none focus:bg-white focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
            placeholder="Search..."
          />
        </div>
      </div>

      {/* Right section */}
      <div className="ml-4 flex items-center space-x-6">
        <div className="relative" ref={notificationRef}>
          <button
            className="text-slate-400 hover:text-slate-500 transition-colors relative"
            onClick={() => setIsNotificationOpen(!isNotificationOpen)}
          >
            <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
            <Bell className="h-5 w-5" />
          </button>

          {/* Notification Dropdown Menu */}
          {isNotificationOpen && (
            <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-slate-100 py-1 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="px-4 py-3 border-b border-slate-100 flex justify-between items-center">
                <p className="text-sm font-semibold text-slate-900">Notifications</p>
                <span className="text-xs text-blue-600 hover:text-blue-700 cursor-pointer font-medium">Mark all read</span>
              </div>
              <div className="max-h-64 overflow-y-auto">
                <div className="px-4 py-3 border-b border-slate-50 hover:bg-slate-50 transition-colors cursor-pointer">
                  <p className="text-sm text-slate-800 font-medium">Leave Request</p>
                  <p className="text-xs text-slate-500 mt-0.5">Jane Doe applied for Sick Leave.</p>
                  <p className="text-[10px] text-slate-400 mt-1">10 minutes ago</p>
                </div>
                <div className="px-4 py-3 border-b border-slate-50 hover:bg-slate-50 transition-colors cursor-pointer bg-blue-50/30">
                  <p className="text-sm text-slate-800 font-medium flex items-center">
                    <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-2"></span>
                    Attendance Alert
                  </p>
                  <p className="text-xs text-slate-500 mt-0.5">3 employees are marked as late today.</p>
                  <p className="text-[10px] text-slate-400 mt-1">1 hour ago</p>
                </div>
                <div className="px-4 py-3 hover:bg-slate-50 transition-colors cursor-pointer">
                  <p className="text-sm text-slate-800 font-medium">System Update</p>
                  <p className="text-xs text-slate-500 mt-0.5">NuruX platform has been updated to v1.2</p>
                  <p className="text-[10px] text-slate-400 mt-1">Yesterday</p>
                </div>
              </div>
              <div className="px-4 py-2 border-t border-slate-100 text-center">
                <button className="text-xs text-slate-500 hover:text-slate-700 font-medium">
                  View all notifications
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="relative" ref={dropdownRef}>
          <div
            className="flex items-center space-x-3 cursor-pointer group"
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
          >
            <div className="h-8 w-8 rounded-full bg-slate-200 overflow-hidden border border-slate-300">
              <img
                src={avatarUrl}
                alt={displayName}
                className="h-full w-full object-cover"
              />
            </div>
            <div className="flex items-center text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">
              <span>{displayName}</span>
              <ChevronDown className="ml-1 h-4 w-4 text-slate-400" />
            </div>
          </div>

          {/* Dropdown Menu */}
          {isDropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-100 py-1 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="px-4 py-2 border-b border-slate-100">
                <p className="text-sm font-medium text-slate-900">{displayName}</p>
                <p className="text-xs text-slate-500 capitalize">{user?.role?.replace('_', ' ') || 'Role not set'}</p>
              </div>
              <button
                onClick={() => {
                  setIsDropdownOpen(false);
                  navigate('/settings');
                }}
                className="w-full text-left px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 flex items-center transition-colors"
              >
                <Settings className="w-4 h-4 mr-2 text-slate-400" />
                Settings
              </button>
              <button
                onClick={handleLogout}
                className="w-full text-left px-4 py-2 text-sm text-rose-600 hover:bg-rose-50 flex items-center transition-colors"
              >
                <LogOut className="w-4 h-4 mr-2 text-rose-500" />
                Sign out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

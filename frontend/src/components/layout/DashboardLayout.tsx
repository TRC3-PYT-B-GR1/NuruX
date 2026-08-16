import React, { useState } from 'react';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
import { AIAssistantWidget } from '../ai/AIAssistantWidget';
import { useSelector } from 'react-redux';
import type { RootState } from '../../store';

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const role = useSelector((state: RootState) => state.auth.user?.role);
  const canUseAi = role && ['super_admin', 'hr_officer', 'manager', 'director'].includes(role);

  return (
    <div className="flex h-screen bg-slate-50 font-sans overflow-hidden">
      <Sidebar isCollapsed={isCollapsed} toggleCollapse={() => setIsCollapsed(!isCollapsed)} />
      <div className={`flex-1 flex flex-col min-w-0 transition-all duration-300 ${isCollapsed ? 'ml-20' : 'ml-64'}`}>
        <TopBar />
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
      {canUseAi && <AIAssistantWidget />}
    </div>
  );
}

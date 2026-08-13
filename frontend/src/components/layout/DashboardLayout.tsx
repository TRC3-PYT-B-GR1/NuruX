import React from 'react';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-slate-50 font-sans overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64 min-w-0">
        <TopBar />
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

import { useState } from 'react';
import { Calendar, CheckCircle, XCircle, Search } from 'lucide-react';
import { useLeave } from '../hooks/useLeave';
import { cn } from '../lib/utils';
import { useSelector } from 'react-redux';
import type { RootState } from '../store';

export function LeaveDashboard() {
  const { requests, isLoading, approveManager, approveHr } = useLeave();
  const [searchTerm, setSearchTerm] = useState('');
  const { user } = useSelector((state: RootState) => state.auth);

  const filteredRequests = requests.filter(req => 
    req.employee_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    req.department_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const pendingRequests = filteredRequests.filter(req => 
    req.status === 'PENDING' || req.status === 'APPROVED_BY_MANAGER'
  );
  
  const historyRequests = filteredRequests.filter(req => 
    req.status !== 'PENDING' && req.status !== 'APPROVED_BY_MANAGER'
  );

  const handleAction = async (id: number, action: 'APPROVE' | 'REJECT', currentStatus: string) => {
    if (user?.role === 'manager' || user?.role === 'director') {
      await approveManager(id, action);
    } else if (user?.role === 'hr_officer' || user?.role === 'super_admin') {
      if (currentStatus === 'APPROVED_BY_MANAGER') {
        await approveHr(id, action);
      } else {
        // HR can also act as manager if bypassing
        await approveManager(id, action);
        if (action === 'APPROVE') {
            await approveHr(id, action); // Double approval for HR overriding
        }
      }
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Leave Management</h1>
        <p className="text-slate-600 mt-1">Review and approve employee time-off requests.</p>
      </div>

      <div className="bg-slate-900/50 backdrop-blur-xl rounded-2xl border border-slate-800 shadow-xl overflow-hidden flex flex-col h-[700px]">
        <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900">
          <h2 className="text-xl font-semibold text-white flex items-center">
            <Calendar className="w-5 h-5 mr-2 text-purple-400" />
            Leave Requests
          </h2>
          <div className="relative w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search by name or department..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
            />
          </div>
        </div>
        
        <div className="flex-1 overflow-auto">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-900/80 sticky top-0 z-10 backdrop-blur-md">
              <tr>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Employee</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Leave Details</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Dates</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Status</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {isLoading ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-400">Loading leave requests...</td>
                </tr>
              ) : filteredRequests.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-400">No requests found.</td>
                </tr>
              ) : (
                [...pendingRequests, ...historyRequests].map(req => (
                  <tr key={req.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-white">{req.employee_name}</div>
                      <div className="text-xs text-slate-400">{req.department_name} • {req.role_title}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-purple-400">{req.leave_type.replace('_', ' ')}</div>
                      <div className="text-xs text-slate-400 truncate max-w-[200px]" title={req.reason}>{req.reason}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-white">{req.start_date}</div>
                      <div className="text-xs text-slate-400">to {req.end_date}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={cn(
                        "inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border",
                        req.status.includes('APPROVED') ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
                        req.status === 'REJECTED' ? "bg-rose-500/10 text-rose-400 border-rose-500/20" :
                        "bg-amber-500/10 text-amber-400 border-amber-500/20"
                      )}>
                        {req.status.replace(/_/g, ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      {req.status === 'PENDING' || (req.status === 'APPROVED_BY_MANAGER' && user?.role === 'hr_officer') ? (
                        <div className="flex justify-end space-x-2">
                          <button 
                            onClick={() => handleAction(req.id, 'APPROVE', req.status)}
                            className="p-1.5 text-emerald-400 hover:bg-emerald-500/20 rounded-md transition-colors"
                            title="Approve"
                          >
                            <CheckCircle className="w-5 h-5" />
                          </button>
                          <button 
                            onClick={() => handleAction(req.id, 'REJECT', req.status)}
                            className="p-1.5 text-rose-400 hover:bg-rose-500/20 rounded-md transition-colors"
                            title="Reject"
                          >
                            <XCircle className="w-5 h-5" />
                          </button>
                        </div>
                      ) : (
                        <span className="text-xs text-slate-500">Processed</span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

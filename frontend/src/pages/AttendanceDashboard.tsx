import { useState } from 'react';
import { Clock, MapPin, Search, AlertCircle, CheckCircle2 } from 'lucide-react';
import { useAttendance } from '../hooks/useAttendance';
import { cn } from '../lib/utils';

export function AttendanceDashboard() {
  const { records, isLoading } = useAttendance();
  const [searchTerm, setSearchTerm] = useState('');

  const filteredRecords = records.filter(record => 
    record.employee_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    record.department_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Attendance Monitoring</h1>
        <p className="text-slate-600 mt-1">Monitor daily clock-ins, clock-outs, and geofencing anomalies.</p>
      </div>

      <div className="bg-slate-900/50 backdrop-blur-xl rounded-2xl border border-slate-800 shadow-xl overflow-hidden flex flex-col h-[700px]">
        <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900">
          <h2 className="text-xl font-semibold text-white flex items-center">
            <Clock className="w-5 h-5 mr-2 text-blue-400" />
            Daily Logs
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
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Date</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Clock In</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Clock Out</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800 text-right">Status / Anomalies</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {isLoading ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-400">Loading attendance records...</td>
                </tr>
              ) : filteredRecords.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-400">No records found.</td>
                </tr>
              ) : (
                filteredRecords.map(record => (
                  <tr key={record.id} className={cn("hover:bg-slate-800/30 transition-colors", record.is_anomaly ? "bg-rose-900/10" : "")}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-white">{record.employee_name}</div>
                      <div className="text-xs text-slate-400">{record.department_name} • {record.role_title}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                      {record.date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-emerald-400">
                        {record.clock_in ? new Date(record.clock_in).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '-'}
                      </div>
                      {record.gps_location_in && (
                        <div className="text-xs text-slate-500 flex items-center mt-1">
                          <MapPin className="w-3 h-3 mr-1" /> {record.gps_location_in}
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-rose-400">
                        {record.clock_out ? new Date(record.clock_out).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '-'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <div className="flex flex-col items-end space-y-2">
                        <span className={cn(
                          "inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border",
                          record.status === 'PRESENT' ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
                          "bg-amber-500/10 text-amber-400 border-amber-500/20"
                        )}>
                          {record.status === 'PRESENT' ? <CheckCircle2 className="w-3 h-3 mr-1" /> : <Clock className="w-3 h-3 mr-1" />}
                          {record.status}
                        </span>
                        
                        {record.is_anomaly && (
                          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border bg-rose-500/10 text-rose-400 border-rose-500/20 max-w-xs truncate" title={record.anomaly_reason}>
                            <AlertCircle className="w-3 h-3 mr-1 flex-shrink-0" />
                            <span className="truncate">{record.anomaly_reason}</span>
                          </span>
                        )}
                      </div>
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

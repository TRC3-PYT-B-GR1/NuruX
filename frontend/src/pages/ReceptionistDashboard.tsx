import { useState, useEffect } from 'react';
import { Clock, QrCode, Search } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { useNavigate } from 'react-router-dom';
import { useTeamAttendance } from '../hooks/useTeamAttendance';
import { Avatar } from '../components/ui/Avatar';

export function ReceptionistDashboard() {
  const navigate = useNavigate();
  const { data: attendance, isLoading } = useTeamAttendance();
  const [searchTerm, setSearchTerm] = useState('');
  const [clockedInList, setClockedInList] = useState<any[]>([]);

  useEffect(() => {
    if (attendance?.todaysAttendance) {
      // Filter for employees currently clocked in
      const present = attendance.todaysAttendance.filter((record: any) => 
        record.clock_in && !record.clock_out
      );
      
      if (searchTerm) {
        setClockedInList(present.filter((r: any) => 
          r.employee_name.toLowerCase().includes(searchTerm.toLowerCase())
        ));
      } else {
        setClockedInList(present);
      }
    }
  }, [attendance, searchTerm]);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Header & Launch Kiosk */}
      <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-indigo-50 rounded-full opacity-50 pointer-events-none" />
        
        <div className="relative z-10 text-center md:text-left">
          <h1 className="text-2xl font-bold text-slate-900">Front Desk Portal</h1>
          <p className="text-sm text-slate-500 mt-1">Manage the office entrance and view who is currently in the building.</p>
        </div>
        
        <Button 
          variant="primary" 
          size="lg"
          className="relative z-10 bg-indigo-600 hover:bg-indigo-700 text-base py-4 px-8 shadow-lg hover:shadow-xl transition-all hover:-translate-y-1"
          onClick={() => navigate('/kiosk')}
        >
          <QrCode className="w-5 h-5 mr-2" />
          <span>Launch QR Kiosk Mode</span>
        </Button>
      </div>

      {/* Live Attendance List */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <h2 className="text-lg font-bold text-slate-800">Currently in Office</h2>
            <span className="text-sm font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">
              {clockedInList.length}
            </span>
          </div>
          
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search active staff..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9 pr-4 py-2 w-full border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
            />
          </div>
        </div>
        
        <div className="p-0">
          {isLoading ? (
            <div className="p-8 text-center text-slate-500">Loading live attendance...</div>
          ) : clockedInList.length === 0 ? (
            <div className="p-12 text-center flex flex-col items-center justify-center">
              <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                <Clock className="w-8 h-8 text-slate-300" />
              </div>
              <h3 className="text-lg font-medium text-slate-900">No one is in the office</h3>
              <p className="text-sm text-slate-500 mt-1">Waiting for staff to clock in today.</p>
            </div>
          ) : (
            <ul className="divide-y divide-slate-100">
              {clockedInList.map((record: any) => (
                <li key={record.id} className="p-4 flex items-center justify-between hover:bg-slate-50 transition-colors">
                  <div className="flex items-center space-x-4">
                    <Avatar alt={record.employee_name} size="md" />
                    <div>
                      <p className="font-semibold text-slate-900">{record.employee_name}</p>
                      <p className="text-xs text-slate-500 flex items-center mt-0.5">
                        <Clock className="w-3 h-3 mr-1" />
                        Clocked in at {new Date(record.clock_in).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                  </div>
                  <div className="px-3 py-1 bg-emerald-50 text-emerald-600 text-xs font-semibold rounded-full">
                    IN OFFICE
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

    </div>
  );
}

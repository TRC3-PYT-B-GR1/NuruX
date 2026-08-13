import { Users, Clock, AlertTriangle, Calendar as CalendarIcon, Loader2, Search, Filter } from 'lucide-react';
import { StatCard } from '../components/ui/StatCard';
import { Avatar } from '../components/ui/Avatar';
import { Table } from '../components/ui/Table';
import { AnomalyCard } from '../components/ui/AnomalyCard';
import { useTeamMembers } from '../hooks/useTeamMembers';
import { useTeamAttendance } from '../hooks/useTeamAttendance';
import { useAnomalies } from '../hooks/useAnomalies';
import { cn } from '../lib/utils';

export function HROfficerDashboard() {
  const { data: teamMembers, isLoading: loadingTeam } = useTeamMembers();
  const { data: attendance, isLoading: loadingAttendance } = useTeamAttendance();
  const { anomalies, isLoading: loadingAnomalies } = useAnomalies();

  if (loadingTeam || loadingAttendance || loadingAnomalies) {
    return (
      <div className="flex items-center justify-center h-full min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin text-indigo-600" />
      </div>
    );
  }

  const tableColumns = [
    {
      header: 'Employee',
      accessor: 'name',
      cell: (row: any) => (
        <div className="flex items-center space-x-3">
          <Avatar alt={row.user.first_name} size="sm" />
          <div>
            <div className="font-medium text-slate-900">{row.user.first_name} {row.user.last_name}</div>
            <div className="text-xs text-slate-500">{row.user.email}</div>
          </div>
        </div>
      )
    },
    {
      header: 'Department',
      accessor: 'department',
      cell: (row: any) => <span className="text-slate-600">{row.department?.name || 'Unassigned'}</span>
    },
    {
      header: 'Role',
      accessor: 'role',
      cell: (row: any) => <span className="text-slate-600">{row.job_title}</span>
    },
    {
      header: 'Status',
      accessor: 'status',
      cell: (row: any) => {
        const isActive = row.is_active;
        return (
          <span className={cn(
            "px-2.5 py-1 text-xs font-medium rounded-full",
            isActive ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-700"
          )}>
            {isActive ? 'Active' : 'Inactive'}
          </span>
        );
      }
    }
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Top Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Total Staff" 
          value={teamMembers?.length || 0} 
          subtitle="All departments" 
          icon={Users} 
          iconBgColor="bg-indigo-50" 
          iconColor="text-indigo-600" 
        />
        <StatCard 
          title="Clocked In" 
          value={attendance?.clockedIn || 0} 
          subtitle="Today"
          icon={Clock} 
          iconBgColor="bg-emerald-50" 
          iconColor="text-emerald-600" 
        />
        <StatCard 
          title="On Leave" 
          value="0" 
          subtitle="Approved today" 
          icon={CalendarIcon} 
          iconBgColor="bg-purple-50" 
          iconColor="text-purple-600" 
        />
        <StatCard 
          title="Anomalies" 
          value={anomalies.length} 
          subtitle="Requires review" 
          icon={AlertTriangle} 
          iconBgColor="bg-rose-50" 
          iconColor="text-rose-600" 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Main Directory Area */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-full">
            <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-bold text-slate-800">Employee Directory</h2>
                <p className="text-sm text-slate-500">Manage all staff members across departments.</p>
              </div>
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-400" />
                  <input 
                    type="text" 
                    placeholder="Search..." 
                    className="pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 w-full sm:w-48"
                  />
                </div>
                <button className="p-2 border border-slate-200 rounded-lg text-slate-500 hover:bg-slate-50">
                  <Filter className="h-4 w-4" />
                </button>
              </div>
            </div>
            
            <div className="p-0 flex-1">
              <Table 
                columns={tableColumns} 
                data={teamMembers || []} 
                className="border-0 shadow-none rounded-none"
              />
            </div>
          </div>
        </div>

        {/* Right Sidebar: Anomalies Review */}
        <div className="space-y-6">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 flex flex-col h-full">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xs font-bold text-slate-800 uppercase tracking-wide flex items-center">
                <AlertTriangle className="h-4 w-4 mr-1.5 text-rose-500" />
                Attendance Review
              </h2>
              <span className="text-xs font-medium text-rose-600 bg-rose-50 px-2 py-1 rounded-full">
                {anomalies.length} Flags
              </span>
            </div>
            
            <div className="space-y-4 flex-1">
              {anomalies.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-48 text-center">
                  <div className="w-12 h-12 bg-emerald-50 rounded-full flex items-center justify-center mb-3">
                    <Clock className="h-6 w-6 text-emerald-500" />
                  </div>
                  <p className="text-sm font-medium text-slate-700">All clear today!</p>
                  <p className="text-xs text-slate-500 mt-1">No GPS or time anomalies detected.</p>
                </div>
              ) : (
                anomalies.map((anomaly) => (
                  <AnomalyCard
                    key={anomaly.id}
                    id={anomaly.id}
                    employeeName={anomaly.employee_name}
                    anomalyReason={anomaly.anomaly_reason || "Unknown Anomaly"}
                    date={anomaly.date}
                    time={anomaly.clock_in ? new Date(anomaly.clock_in).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : null}
                    onApprove={(id) => console.log('Dismiss anomaly', id)}
                    onFlag={(id) => console.log('Investigate anomaly', id)}
                  />
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

import { useState } from 'react';
import { Download, FileText, Filter, QrCode, Search, TrendingUp, Users } from 'lucide-react';
import { StatCard } from '../components/ui/StatCard';
import { Button } from '../components/ui/Button';
import { useNavigate } from 'react-router-dom';
import { useTeamAttendance } from '../hooks/useTeamAttendance';
import { useAnomalies } from '../hooks/useAnomalies';
import { Table } from '../components/ui/Table';

export function ReportsPage() {
  const navigate = useNavigate();
  const { data: attendance, isLoading: loadingAttendance } = useTeamAttendance();
  const { anomalies, isLoading: loadingAnomalies } = useAnomalies();
  const [activeTab, setActiveTab] = useState<'attendance' | 'anomalies'>('attendance');

  const attendanceColumns = [
    {
      header: 'Employee',
      accessor: 'employee_name',
      cell: (row: any) => <span className="font-medium text-slate-900">{row.employee_name}</span>
    },
    {
      header: 'Date',
      accessor: 'date',
      cell: (row: any) => <span className="text-slate-600">{row.date}</span>
    },
    {
      header: 'Clock In',
      accessor: 'clock_in',
      cell: (row: any) => <span className="text-slate-600">{row.clock_in ? new Date(row.clock_in).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '-'}</span>
    },
    {
      header: 'Clock Out',
      accessor: 'clock_out',
      cell: (row: any) => <span className="text-slate-600">{row.clock_out ? new Date(row.clock_out).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '-'}</span>
    },
    {
      header: 'Status',
      accessor: 'status',
      cell: (row: any) => (
        <span className={`px-2.5 py-1 text-xs font-medium rounded-full ${
          row.status === 'PRESENT' ? 'bg-emerald-100 text-emerald-700' : 
          row.status === 'LATE' ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-700'
        }`}>
          {row.status}
        </span>
      )
    }
  ];

  const anomalyColumns = [
    {
      header: 'Employee',
      accessor: 'employee_name',
      cell: (row: any) => <span className="font-medium text-slate-900">{row.employee_name}</span>
    },
    {
      header: 'Date & Time',
      accessor: 'date',
      cell: (row: any) => (
        <div className="flex flex-col">
          <span className="text-slate-900 text-sm">{row.date}</span>
          <span className="text-slate-500 text-xs">{row.clock_in ? new Date(row.clock_in).toLocaleTimeString() : '-'}</span>
        </div>
      )
    },
    {
      header: 'Anomaly Reason',
      accessor: 'anomaly_reason',
      cell: (row: any) => <span className="text-rose-600 font-medium text-xs bg-rose-50 px-2 py-1 rounded">{row.anomaly_reason}</span>
    },
    {
      header: 'Action',
      accessor: 'id',
      cell: () => (
        <Button variant="outline" size="sm" className="text-xs">Investigate</Button>
      )
    }
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Header & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Reports & Analytics</h1>
          <p className="text-sm text-slate-500 mt-1">Generate payroll reports and audit attendance anomalies.</p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline" className="flex items-center space-x-2">
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </Button>
          <Button 
            variant="primary" 
            className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700"
            onClick={() => navigate('/kiosk')}
          >
            <QrCode className="w-4 h-4" />
            <span>Launch QR Kiosk</span>
          </Button>
        </div>
      </div>

      {/* High Level Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard 
          title="Total Reports" 
          value="24" 
          subtitle="Generated this month" 
          icon={FileText} 
          iconBgColor="bg-blue-50" 
          iconColor="text-blue-600" 
        />
        <StatCard 
          title="Average Attendance" 
          value="94%" 
          subtitle="+2% from last month" 
          icon={TrendingUp} 
          iconBgColor="bg-emerald-50" 
          iconColor="text-emerald-600" 
        />
        <StatCard 
          title="Flagged Anomalies" 
          value={anomalies.length} 
          subtitle="Pending review" 
          icon={Users} 
          iconBgColor="bg-rose-50" 
          iconColor="text-rose-600" 
        />
      </div>

      {/* Data Section */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="border-b border-slate-200">
          <div className="flex px-6">
            <button 
              className={`py-4 px-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'attendance' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}`}
              onClick={() => setActiveTab('attendance')}
            >
              Timesheets
            </button>
            <button 
              className={`py-4 px-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'anomalies' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}`}
              onClick={() => setActiveTab('anomalies')}
            >
              Audit Log (Anomalies)
            </button>
          </div>
        </div>
        
        <div className="p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 bg-slate-50/50">
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search records..." 
              className="pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 w-full bg-white"
            />
          </div>
          <Button variant="outline" className="text-sm bg-white">
            <Filter className="w-4 h-4 mr-2" />
            Filter by Date
          </Button>
        </div>

        <div className="p-0">
          {activeTab === 'attendance' ? (
            <Table 
              columns={attendanceColumns} 
              data={attendance?.raw || []} 
              isLoading={loadingAttendance}
              className="border-0 shadow-none rounded-none"
            />
          ) : (
            <Table 
              columns={anomalyColumns} 
              data={anomalies || []} 
              isLoading={loadingAnomalies}
              className="border-0 shadow-none rounded-none"
            />
          )}
        </div>
      </div>
    </div>
  );
}

import { Users, Clock, AlertCircle, Calendar as CalendarIcon, Loader2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { StatCard } from '../components/ui/StatCard';
import { Avatar } from '../components/ui/Avatar';
import { Button } from '../components/ui/Button';
import { cn } from '../lib/utils';
import { useTeamMembers } from '../hooks/useTeamMembers';
import { useTeamAttendance } from '../hooks/useTeamAttendance';
import { useLeaveApprovals, useApproveLeave } from '../hooks/useLeaveApprovals';

export function ManagerDashboard() {
  const { data: teamMembers, isLoading: loadingTeam } = useTeamMembers();
  const { data: attendance, isLoading: loadingAttendance } = useTeamAttendance();
  const { data: leaveApprovals, isLoading: loadingLeave } = useLeaveApprovals();
  const approveLeave = useApproveLeave();

  if (loadingTeam || loadingAttendance || loadingLeave) {
    return (
      <div className="flex items-center justify-center h-full min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  // Formatting team status from attendance and leave data (simplified for demo)
  const teamStatus = teamMembers?.map((member) => {
    const todayAttendance = attendance?.todaysAttendance.find(a => a.employee_name === member.user.first_name + ' ' + member.user.last_name);
    
    let status = 'Not clocked in';
    let isLate = false;
    let isLeave = false;
    let time = '';

    if (todayAttendance) {
      if (todayAttendance.status === 'LATE') {
        isLate = true;
        status = 'Running late';
        time = todayAttendance.clock_in ? new Date(todayAttendance.clock_in).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '';
      } else if (todayAttendance.clock_in) {
        status = `Clocked in - ${new Date(todayAttendance.clock_in).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}`;
        time = new Date(todayAttendance.clock_in).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
      }
    } else {
      // Check leave (simplified, assuming we had a way to check if on leave today)
    }

    return {
      id: member.id,
      name: `${member.user.first_name} ${member.user.last_name}`,
      role: member.job_title,
      status,
      time,
      avatar: `https://ui-avatars.com/api/?name=${member.user.first_name}+${member.user.last_name}&background=random`,
      isLate,
      isLeave
    };
  }) || [];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Team Members" 
          value={teamMembers?.length || 0} 
          subtitle="Total" 
          icon={Users} 
          iconBgColor="bg-blue-50" 
          iconColor="text-blue-600" 
        />
        <StatCard 
          title="Clocked In" 
          value={attendance?.clockedIn || 0} 
          subtitle={`${Math.round(((attendance?.clockedIn || 0) / (teamMembers?.length || 1)) * 100)}% attendance`}
          icon={Clock} 
          iconBgColor="bg-emerald-50" 
          iconColor="text-emerald-600" 
        />
        <StatCard 
          title="Running Late" 
          value={attendance?.runningLate || 0} 
          subtitle={attendance?.runningLate ? "Needs attention" : "All good"}
          icon={AlertCircle} 
          iconBgColor="bg-amber-50" 
          iconColor="text-amber-600" 
        />
        <StatCard 
          title="On Leave" 
          value="0" // Placeholder
          subtitle="Today" 
          icon={CalendarIcon} 
          iconBgColor="bg-purple-50" 
          iconColor="text-purple-600" 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Today's Team Status (Timeline) */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-sm p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-bold text-slate-800 uppercase tracking-wide text-xs">Today's Team Status</h2>
            <div className="flex items-center space-x-2">
              <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-xs text-slate-500 font-medium">Live</span>
            </div>
          </div>
          
          <div className="space-y-8 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
            {teamStatus.map((item) => (
              <div key={item.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                {/* Timeline dot */}
                <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-slate-100 text-slate-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <span className="text-[10px] font-semibold">{item.time || '-'}</span>
                </div>
                
                {/* Content */}
                <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-slate-100 bg-white shadow-sm transition-all hover:shadow-md">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <Avatar src={item.avatar} alt={item.name} size="md" />
                      <div>
                        <h4 className="text-sm font-bold text-slate-900">{item.name}</h4>
                        <p className="text-xs text-slate-500">{item.role}</p>
                      </div>
                    </div>
                  </div>
                  <div className="mt-3">
                    <span className={cn(
                      "text-xs font-medium",
                      item.isLate ? "text-rose-600" : item.isLeave ? "text-slate-500" : "text-emerald-600"
                    )}>
                      {item.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          
          {/* Approval Inbox */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xs font-bold text-slate-800 uppercase tracking-wide">Approval Inbox</h2>
              <span className="text-xs text-slate-500">{leaveApprovals?.length || 0} pending</span>
            </div>
            
            <div className="space-y-4">
              {leaveApprovals?.length === 0 ? (
                <p className="text-sm text-slate-500 text-center py-4">No pending approvals.</p>
              ) : (
                leaveApprovals?.map((request) => (
                  <div key={request.id} className="p-4 rounded-lg border border-slate-100 bg-slate-50 hover:bg-slate-100 transition-colors">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex items-center space-x-3">
                        <Avatar alt={request.employee_name} size="sm" />
                        <div>
                          <h4 className="text-sm font-bold text-slate-900">{request.employee_name}</h4>
                          <p className="text-xs text-slate-500">{request.leave_type} • {request.start_date}</p>
                        </div>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <Button 
                        variant="primary" 
                        size="sm" 
                        className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-xs py-1.5"
                        onClick={() => approveLeave.mutate({ id: request.id, action: 'APPROVE' })}
                        disabled={approveLeave.isPending}
                      >
                        Approve
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="flex-1 text-xs py-1.5 text-rose-600 hover:text-rose-700 hover:bg-rose-50"
                        onClick={() => approveLeave.mutate({ id: request.id, action: 'REJECT' })}
                        disabled={approveLeave.isPending}
                      >
                        Reject
                      </Button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Team Attendance Bar Chart */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
            <h2 className="text-xs font-bold text-slate-800 uppercase tracking-wide mb-6">Team Attendance This Week</h2>
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={attendance?.weeklyData || []} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} />
                  <Tooltip 
                    cursor={{fill: '#f8fafc'}}
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Legend iconType="circle" wrapperStyle={{ fontSize: '10px' }} />
                  <Bar dataKey="present" name="Present" fill="#10b981" radius={[2, 2, 0, 0]} barSize={12} />
                  <Bar dataKey="late" name="Late" fill="#f59e0b" radius={[2, 2, 0, 0]} barSize={12} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

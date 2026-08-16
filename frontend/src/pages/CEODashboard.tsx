import { useCEOMetrics } from '../hooks/useCEOMetrics';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Cell
} from 'recharts';
import { AIInsightsCard } from '../components/ai/AIInsightsCard';

export default function CEODashboard() {
  const { metrics, loading, error } = useCEOMetrics();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error || !metrics) {
    return (
      <div className="flex items-center justify-center h-full text-red-500">
        Error loading metrics: {error}
      </div>
    );
  }

  const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#14b8a6', '#f59e0b'];

  return (
    <div className="p-8 space-y-8 fade-in">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
            Executive Overview
          </h1>
          <p className="text-gray-500 mt-1">Real-time company performance metrics.</p>
        </div>
      </div>

      {/* AI Insights */}
      <AIInsightsCard />

      {/* Top Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard 
          title="Total Headcount" 
          value={metrics.total_employees} 
          icon="👥"
          gradient="from-indigo-500/10 to-purple-500/10"
          border="border-indigo-100"
        />
        <MetricCard 
          title="Monthly Payroll" 
          value={`₦${metrics.total_monthly_payroll.toLocaleString()}`} 
          icon="💰"
          gradient="from-emerald-500/10 to-teal-500/10"
          border="border-emerald-100"
        />
        <MetricCard 
          title="Today's Attendance" 
          value={`${metrics.attendance_rate}%`} 
          icon="📊"
          gradient="from-amber-500/10 to-orange-500/10"
          border="border-amber-100"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Department Breakdown Chart */}
        <div className="lg:col-span-2 glass p-6 rounded-2xl border border-white/20 shadow-lg relative overflow-hidden group hover:-translate-y-1 transition-transform duration-300">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-50/50 to-purple-50/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <h3 className="text-xl font-semibold mb-6 text-gray-800 relative z-10">Department Headcount</h3>
          <div className="h-72 w-full relative z-10">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={metrics.department_breakdown}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                <XAxis 
                  dataKey="name" 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fill: '#6b7280', fontSize: 12 }}
                  dy={10}
                />
                <YAxis 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fill: '#6b7280', fontSize: 12 }}
                  dx={-10}
                />
                <Tooltip 
                  cursor={{ fill: '#f3f4f6' }}
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)' }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]} maxBarSize={50}>
                  {metrics.department_breakdown.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Payroll Runs */}
        <div className="glass p-6 rounded-2xl border border-white/20 shadow-lg relative overflow-hidden group hover:-translate-y-1 transition-transform duration-300">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-50/50 to-purple-50/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <h3 className="text-xl font-semibold mb-6 text-gray-800 relative z-10">Recent Payrolls</h3>
          <div className="space-y-4 relative z-10">
            {metrics.recent_payroll_runs.length > 0 ? (
              metrics.recent_payroll_runs.map((run) => (
                <div key={run.id} className="flex items-center justify-between p-4 rounded-xl bg-white/40 border border-white/50 backdrop-blur-sm">
                  <div className="flex items-center space-x-3">
                    <div className="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600">
                      📄
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{run.month}</p>
                      <p className="text-sm text-gray-500">
                        {run.is_finalized ? 'Finalized' : 'Processing'}
                      </p>
                    </div>
                  </div>
                  <span className={`px-2.5 py-1 text-xs font-medium rounded-full ${
                    run.is_finalized ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {run.is_finalized ? 'Completed' : 'Pending'}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-sm">No recent payroll runs.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, gradient, border }: { title: string, value: string | number, icon: string, gradient: string, border: string }) {
  return (
    <div className={`glass p-6 rounded-2xl border border-white/20 shadow-lg relative overflow-hidden group hover:-translate-y-1 transition-transform duration-300 bg-gradient-to-br ${gradient}`}>
      <div className="flex justify-between items-start">
        <div>
          <p className="text-gray-500 font-medium mb-1">{title}</p>
          <h2 className="text-3xl font-bold text-gray-900">{value}</h2>
        </div>
        <div className={`h-12 w-12 rounded-xl bg-white flex items-center justify-center text-2xl shadow-sm border ${border}`}>
          {icon}
        </div>
      </div>
      <div className="absolute -bottom-4 -right-4 h-24 w-24 bg-white/20 rounded-full blur-2xl group-hover:bg-white/30 transition-colors"></div>
    </div>
  );
}

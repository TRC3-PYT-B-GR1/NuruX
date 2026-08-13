import type { LucideIcon } from 'lucide-react';
import { cn } from '../../lib/utils';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  iconBgColor?: string;
  iconColor?: string;
  trend?: {
    value: string;
    isPositive: boolean;
  };
}

export function StatCard({ 
  title, 
  value, 
  subtitle, 
  icon: Icon,
  iconBgColor = 'bg-blue-50',
  iconColor = 'text-blue-600',
  trend
}: StatCardProps) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">{title}</h3>
          <div className="text-3xl font-bold text-slate-900">{value}</div>
        </div>
        <div className={cn("p-3 rounded-full flex items-center justify-center", iconBgColor)}>
          <Icon className={cn("h-6 w-6", iconColor)} />
        </div>
      </div>
      
      <div className="flex items-center mt-2">
        {trend && (
          <span className={cn(
            "text-sm font-medium mr-2",
            trend.isPositive ? "text-emerald-600" : "text-rose-600"
          )}>
            {trend.isPositive ? '↑' : '↓'} {trend.value}
          </span>
        )}
        {subtitle && (
          <span className="text-sm text-slate-500">{subtitle}</span>
        )}
      </div>
    </div>
  );
}

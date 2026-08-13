import { AlertTriangle, MapPin, Clock } from 'lucide-react';
import { Avatar } from './Avatar';
import { Button } from './Button';

interface AnomalyCardProps {
  id: number;
  employeeName: string;
  avatarUrl?: string;
  anomalyReason: string;
  date: string;
  time: string | null;
  onApprove: (id: number) => void;
  onFlag: (id: number) => void;
}

export function AnomalyCard({ id, employeeName, avatarUrl, anomalyReason, date, time, onApprove, onFlag }: AnomalyCardProps) {
  // Determine if it's a GPS or Time anomaly for the icon
  const isGPS = anomalyReason.toLowerCase().includes('gps') || anomalyReason.toLowerCase().includes('location');
  
  return (
    <div className="p-4 rounded-xl border border-rose-100 bg-rose-50 shadow-sm relative overflow-hidden group">
      <div className="absolute top-0 left-0 w-1 h-full bg-rose-500"></div>
      
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center space-x-3">
          <Avatar alt={employeeName} src={avatarUrl} size="sm" />
          <div>
            <h4 className="text-sm font-bold text-slate-900">{employeeName}</h4>
            <p className="text-xs text-slate-500">{date} {time ? `• ${time}` : ''}</p>
          </div>
        </div>
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-rose-100 text-rose-600">
          {isGPS ? <MapPin className="w-4 h-4" /> : <Clock className="w-4 h-4" />}
        </div>
      </div>
      
      <div className="mb-4">
        <p className="text-xs font-medium text-rose-700 bg-rose-100/50 p-2 rounded-md border border-rose-100">
          <AlertTriangle className="inline w-3 h-3 mr-1 -mt-0.5" />
          {anomalyReason}
        </p>
      </div>
      
      <div className="flex space-x-2">
        <Button 
          variant="outline" 
          size="sm" 
          className="flex-1 text-xs py-1.5 border-rose-200 text-rose-700 hover:bg-rose-100"
          onClick={() => onFlag(id)}
        >
          Investigate
        </Button>
        <Button 
          variant="primary" 
          size="sm" 
          className="flex-1 bg-slate-800 hover:bg-slate-900 text-xs py-1.5"
          onClick={() => onApprove(id)}
        >
          Dismiss
        </Button>
      </div>
    </div>
  );
}

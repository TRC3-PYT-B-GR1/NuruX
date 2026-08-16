import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import { endOfWeek, format, isWithinInterval, parseISO, startOfWeek } from 'date-fns';

export interface AttendanceRecord {
  id: number;
  employee_name: string;
  date: string;
  clock_in: string | null;
  clock_out: string | null;
  status: string;
  is_anomaly: boolean;
  anomaly_reason: string | null;
}

export function useTeamAttendance() {
  return useQuery({
    queryKey: ['attendance'],
    queryFn: async () => {
      const response = await api.get('/attendance/attendance/');
      return (response.data.results ? response.data.results : response.data) as AttendanceRecord[];
    },
    select: (data) => {
      // Process data for the dashboard charts and widgets
      const today = new Date();
      const todayStr = format(today, 'yyyy-MM-dd');
      
      const todaysAttendance = data.filter((record) => record.date === todayStr);
      const clockedIn = todaysAttendance.filter((record) => record.clock_in && !record.clock_out).length;
      const runningLate = todaysAttendance.filter((record) => record.status === 'LATE').length;
      
      // Calculate weekly data (dummy calculation for now, just mapping the days)
      const weeklyData = [
        { name: 'Mon', present: 0, late: 0, absent: 0 },
        { name: 'Tue', present: 0, late: 0, absent: 0 },
        { name: 'Wed', present: 0, late: 0, absent: 0 },
        { name: 'Thu', present: 0, late: 0, absent: 0 },
        { name: 'Fri', present: 0, late: 0, absent: 0 },
        { name: 'Sat', present: 0, late: 0, absent: 0 },
        { name: 'Sun', present: 0, late: 0, absent: 0 },
      ];
      
      const currentWeek = {
        start: startOfWeek(today, { weekStartsOn: 1 }),
        end: endOfWeek(today, { weekStartsOn: 1 }),
      };
      data
        .filter((record) => isWithinInterval(parseISO(record.date), currentWeek))
        .forEach((record) => {
        const d = new Date(record.date);
        const dayIndex = (d.getDay() + 6) % 7; // Make Monday 0
        
        if (record.status === 'PRESENT') weeklyData[dayIndex].present++;
        if (record.status === 'LATE') weeklyData[dayIndex].late++;
        if (record.status === 'ABSENT') weeklyData[dayIndex].absent++;
        });

      return {
        raw: data,
        todaysAttendance,
        clockedIn,
        runningLate,
        weeklyData
      };
    }
  });
}

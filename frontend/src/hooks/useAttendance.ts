import { useState, useEffect, useCallback } from 'react';
import { api } from '../lib/api';

export interface AttendanceRecord {
  id: number;
  employee: number;
  employee_name: string;
  department_name: string;
  role_title: string;
  date: string;
  clock_in: string | null;
  clock_out: string | null;
  gps_location_in: string | null;
  gps_location_out: string | null;
  status: string;
  is_anomaly: boolean;
  anomaly_reason: string;
}

export function useAttendance() {
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchRecords = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await api.get('/attendance/attendance/');
      const data = res.data.results ? res.data.results : res.data;
      setRecords(data);
    } catch (error) {
      console.error('Error fetching attendance:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRecords();
  }, [fetchRecords]);

  return { records, isLoading, refetch: fetchRecords };
}

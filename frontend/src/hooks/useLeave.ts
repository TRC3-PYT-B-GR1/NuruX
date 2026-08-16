import { useState, useEffect, useCallback } from 'react';
import { api } from '../lib/api';

export interface LeaveRequest {
  id: number;
  employee: number;
  employee_name: string;
  department_name: string;
  role_title: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: string;
  manager_approver: number | null;
  manager_approver_name: string;
  hr_approver: number | null;
  hr_approver_name: string;
  created_at: string;
}

export function useLeave() {
  const [requests, setRequests] = useState<LeaveRequest[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchRequests = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await api.get('/leave/leave-requests/');
      const data = res.data.results ? res.data.results : res.data;
      setRequests(data);
    } catch (error) {
      console.error('Error fetching leave requests:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRequests();
  }, [fetchRequests]);

  const approveManager = async (id: number, action: 'APPROVE' | 'REJECT') => {
    await api.post(`/leave/leave-requests/${id}/approve_manager/`, { action });
    await fetchRequests();
  };

  const approveHr = async (id: number, action: 'APPROVE' | 'REJECT') => {
    await api.post(`/leave/leave-requests/${id}/approve_hr/`, { action });
    await fetchRequests();
  };

  return { requests, isLoading, approveManager, approveHr, refetch: fetchRequests };
}

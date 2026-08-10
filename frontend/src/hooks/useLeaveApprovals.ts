import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

export interface LeaveRequest {
  id: number;
  employee: number;
  employee_name: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: string;
  created_at: string;
}

export function useLeaveApprovals() {
  return useQuery({
    queryKey: ['leave-requests', 'pending'],
    queryFn: async () => {
      const response = await api.get<LeaveRequest[]>('/leave-requests/');
      // Filter for PENDING requests on the client side since we don't have a specific endpoint filter yet
      return response.data.filter(req => req.status === 'PENDING');
    }
  });
}

export function useApproveLeave() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ id, action }: { id: number, action: 'APPROVE' | 'REJECT' }) => {
      const response = await api.post(`/leave-requests/${id}/approve_manager/`, { action });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['leave-requests'] });
    }
  });
}

import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';

export interface Employee {
  id: number;
  user: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
  };
  department: {
    id: number;
    name: string;
  };
  employee_id: string;
  job_title: string;
  hire_date: string;
  is_active: boolean;
}

export function useTeamMembers() {
  return useQuery({
    queryKey: ['employees'],
    queryFn: async () => {
      const response = await api.get<Employee[]>('/employees/');
      return response.data;
    }
  });
}

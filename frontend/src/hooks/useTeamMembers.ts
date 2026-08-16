import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';

export interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  department_details: {
    id: number;
    name: string;
  } | null;
  role_details: {
    id: number;
    title: string;
  } | null;
  status: string;
  date_joined: string | null;
}

export function useTeamMembers() {
  return useQuery({
    queryKey: ['employees'],
    queryFn: async () => {
      const response = await api.get('/employees/');
      return (response.data.results ? response.data.results : response.data) as Employee[];
    }
  });
}

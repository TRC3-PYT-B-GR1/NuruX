import { useState, useEffect, useCallback } from 'react';
import { api } from '../lib/api';

export interface EmployeeMetrics {
  total_headcount: number;
  total_departments: number;
  headcount_by_department: { name: string; count: number }[];
  total_clock_ins: number;
  clock_ins_by_department: { name: string; count: number }[];
  total_clock_outs: number;
  clock_outs_by_department: { name: string; count: number }[];
}

export interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  status: string;
  date_joined: string;
  department_details: { id: number; name: string };
  role_details: { id: number; title: string };
}

export function useEmployees() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [metrics, setMetrics] = useState<EmployeeMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchEmployees = useCallback(async () => {
    setIsLoading(true);
    try {
      const [empRes, metricsRes] = await Promise.all([
        api.get('/employees/'),
        api.get('/employees/metrics/')
      ]);
      const empData = empRes.data.results ? empRes.data.results : empRes.data;
      setEmployees(empData);
      setMetrics(metricsRes.data);
    } catch (error) {
      console.error('Error fetching employees:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchEmployees();
  }, [fetchEmployees]);

  const addEmployee = async (data: any) => {
    await api.post('/employees/', data);
    await fetchEmployees();
  };

  return { employees, metrics, isLoading, addEmployee, refetch: fetchEmployees };
}

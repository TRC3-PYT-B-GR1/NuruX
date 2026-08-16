import { useState, useEffect, useCallback } from 'react';
import { api } from '../lib/api';

export interface Department {
  id: number;
  name: string;
  description: string;
}

export function useDepartments() {
  const [departments, setDepartments] = useState<Department[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchDepartments = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await api.get('/organizations/departments/');
      const data = res.data.results ? res.data.results : res.data;
      setDepartments(data);
    } catch (error) {
      console.error('Error fetching departments:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDepartments();
  }, [fetchDepartments]);

  const addDepartment = async (data: any) => {
    await api.post('/organizations/departments/', data);
    await fetchDepartments();
  };

  return { departments, isLoading, addDepartment, refetch: fetchDepartments };
}

import { useState, useEffect, useCallback } from 'react';
import { api } from '../lib/api';

export interface Role {
  id: number;
  title: string;
}

export function useRoles() {
  const [roles, setRoles] = useState<Role[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchRoles = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await api.get('/organizations/roles/');
      const data = res.data.results ? res.data.results : res.data;
      setRoles(data);
    } catch (error) {
      console.error('Error fetching roles:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const addRole = useCallback(async (data: { title: string; department: number }) => {
    try {
      const res = await api.post('/organizations/roles/', data);
      await fetchRoles();
      return res.data;
    } catch (error) {
      console.error('Error adding role:', error);
      throw error;
    }
  }, [fetchRoles]);

  useEffect(() => {
    fetchRoles();
  }, [fetchRoles]);

  return { roles, isLoading, refetch: fetchRoles, addRole };
}

import { useState, useEffect } from 'react';
import { api } from '../lib/api';

export interface CEOMetrics {
  total_employees: number;
  attendance_rate: number;
  total_monthly_payroll: number;
  department_breakdown: {
    name: string;
    count: number;
  }[];
  recent_payroll_runs: {
    id: number;
    month: string;
    is_finalized: boolean;
  }[];
}

export function useCEOMetrics() {
  const [metrics, setMetrics] = useState<CEOMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchMetrics() {
      try {
        const response = await api.get('/organizations/ceo-metrics/');
        setMetrics(response.data);
        setError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch CEO metrics');
      } finally {
        setLoading(false);
      }
    }

    fetchMetrics();
  }, []);

  return { metrics, loading, error };
}

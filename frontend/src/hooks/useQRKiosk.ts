import { useState, useEffect, useCallback } from 'react';
import { api } from '../lib/api';

export function useQRKiosk() {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [timeLeft, setTimeLeft] = useState<number>(60);
  const [error, setError] = useState<string | null>(null);

  const fetchToken = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await api.get('/attendance/attendance/generate_qr/');
      setToken(response.data.qr_token);
      setTimeLeft(60);
    } catch (err: any) {
      console.error('Failed to fetch QR token:', err);
      setError(err.response?.data?.detail || 'Failed to fetch token');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchToken();

    // Fetch a new token every 60 seconds
    const intervalId = setInterval(() => {
      fetchToken();
    }, 60000);

    return () => clearInterval(intervalId);
  }, [fetchToken]);

  useEffect(() => {
    // Countdown timer for the UI
    const timerId = setInterval(() => {
      setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);

    return () => clearInterval(timerId);
  }, []);

  return { token, isLoading, timeLeft, error, refetch: fetchToken };
}

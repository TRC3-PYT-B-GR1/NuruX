import axios, { type InternalAxiosRequestConfig } from 'axios';

const configuredBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
export const API_BASE_URL = configuredBaseUrl.replace(/\/$/, '');

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

interface RetryableRequest extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

let refreshPromise: Promise<string> | null = null;

function clearSession() {
  localStorage.removeItem('nuru_access_token');
  localStorage.removeItem('nuru_refresh_token');
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('nuru_access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config as RetryableRequest | undefined;
    const refresh = localStorage.getItem('nuru_refresh_token');
    const isRefreshRequest = original?.url?.includes('/accounts/refresh/');

    if (error.response?.status !== 401 || !original || original._retry || !refresh || isRefreshRequest) {
      return Promise.reject(error);
    }

    original._retry = true;
    try {
      refreshPromise ??= axios
        .post(`${API_BASE_URL}/accounts/refresh/`, { refresh })
        .then(({ data }) => {
          localStorage.setItem('nuru_access_token', data.access);
          if (data.refresh) localStorage.setItem('nuru_refresh_token', data.refresh);
          return data.access as string;
        })
        .finally(() => {
          refreshPromise = null;
        });
      const access = await refreshPromise;
      original.headers.Authorization = `Bearer ${access}`;
      return api(original);
    } catch (refreshError) {
      clearSession();
      if (window.location.pathname !== '/login') window.location.assign('/login');
      return Promise.reject(refreshError);
    }
  },
);

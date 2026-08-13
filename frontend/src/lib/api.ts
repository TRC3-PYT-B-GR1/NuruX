import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Temporary auth bypass interceptor
// Normally this would grab the token from localStorage or a context provider
api.interceptors.request.use((config) => {
  // We will manually acquire a token and paste it here for this phase,
  // or use basic auth if we create a superuser.
  // Actually, since we want to bypass login, we can just use a hardcoded token.
  const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg2MzkzOTUwLCJpYXQiOjE3ODYzOTMwNTAsImp0aSI6ImEwMTVjYTlmYTEyZTQzYzU4ODk2YTE3YWVmYzYzYTNmIiwidXNlcl9pZCI6IjEifQ.X1eBOGroYnc4K_Q8rvtCGLRrT9LM1Pvq1n9f2WfrsYA';
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

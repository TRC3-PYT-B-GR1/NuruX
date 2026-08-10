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
  const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg2Mjc5NTI3LCJpYXQiOjE3ODYyNzkyMjcsImp0aSI6IjIyYTQwYzM1ZWNhMDQxMGU4M2M0N2M3YWRlZTE1YzI1IiwidXNlcl9pZCI6IjEzIn0.FwyRv5jqXfhg6h9FluwH6S_LtrWEkTo74ZLbzUMXdpc';
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

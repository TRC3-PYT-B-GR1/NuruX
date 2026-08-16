import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export type Role = 'super_admin' | 'hr_officer' | 'manager' | 'payroll_officer' | 'director' | 'employee' | 'applicant' | 'receptionist';

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  role?: Role;
  department?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Check local storage for initial token
const initialToken = localStorage.getItem('nuru_access_token');

const initialState: AuthState = {
  user: null,
  token: initialToken,
  isAuthenticated: !!initialToken,
  isLoading: false,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials: (
      state,
      action: PayloadAction<{ user: User; access: string; refresh: string }>
    ) => {
      const { user, access, refresh } = action.payload;
      state.user = user;
      state.token = access;
      state.isAuthenticated = true;
      localStorage.setItem('nuru_access_token', access);
      localStorage.setItem('nuru_refresh_token', refresh);
    },
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
      localStorage.removeItem('nuru_access_token');
      localStorage.removeItem('nuru_refresh_token');
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    }
  },
});

export const { setCredentials, setUser, logout, setLoading } = authSlice.actions;
export default authSlice.reducer;

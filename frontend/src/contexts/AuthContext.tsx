import React, { createContext, useEffect, useState } from 'react';
import { User, AuthState } from '../types';

interface AuthContextType extends AuthState {
  login: (token: string, user: User) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: localStorage.getItem('forecastiq_token'),
    isAuthenticated: false,
    isLoading: true,
  });

  useEffect(() => {
    // Initializing auth state check from local storage token
    const token = localStorage.getItem('forecastiq_token');
    if (token) {
      setState((prev) => ({ ...prev, token, isAuthenticated: true, isLoading: false }));
    } else {
      setState((prev) => ({ ...prev, isLoading: false }));
    }
  }, []);

  const login = (token: string, user: User) => {
    localStorage.setItem('forecastiq_token', token);
    setState({
      user,
      token,
      isAuthenticated: true,
      isLoading: false,
    });
  };

  const logout = () => {
    localStorage.removeItem('forecastiq_token');
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

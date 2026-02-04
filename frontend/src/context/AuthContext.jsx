import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const userData = await authAPI.getCurrentUser();
        setUser(userData);
      } catch (error) {
        localStorage.removeItem('access_token');
      }
    }
    setLoading(false);
  };

  const login = async (username, password) => {
    const data = await authAPI.login(username, password);
    localStorage.setItem('access_token', data.access_token);
    const userData = await authAPI.getCurrentUser();
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  const register = async (userData) => {
    await authAPI.register(userData);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
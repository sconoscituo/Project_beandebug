import apiClient from './client';

export const beansAPI = {
  getMyBeans: async (params = {}) => {
    const response = await apiClient.get('/beans/', { params });
    return response.data;
  },

  getPublicBeans: async (params = {}) => {
    const response = await apiClient.get('/beans/public', { params });
    return response.data;
  },

  getBean: async (id) => {
    const response = await apiClient.get(`/beans/${id}`);
    return response.data;
  },

  createBean: async (beanData) => {
    const response = await apiClient.post('/beans/', beanData);
    return response.data;
  },

  updateBean: async (id, beanData) => {
    const response = await apiClient.put(`/beans/${id}`, beanData);
    return response.data;
  },

  deleteBean: async (id) => {
    await apiClient.delete(`/beans/${id}`);
  },
};
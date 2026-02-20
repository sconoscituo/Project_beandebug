import apiClient from './client';

export const articlesAPI = {
  getArticles: async (params = {}) => {
    const response = await apiClient.get('/articles/', { params });
    return response.data;
  },

  getArticle: async (id) => {
    const response = await apiClient.get(`/articles/${id}`);
    return response.data;
  },

  getMyArticles: async (params = {}) => {
    const response = await apiClient.get('/articles/my', { params });
    return response.data;
  },

  createArticle: async (articleData) => {
    const response = await apiClient.post('/articles/', articleData);
    return response.data;
  },

  updateArticle: async (id, articleData) => {
    const response = await apiClient.put(`/articles/${id}`, articleData);
    return response.data;
  },

  deleteArticle: async (id) => {
    await apiClient.delete(`/articles/${id}`);
  },

  likeArticle: async (id) => {
    const response = await apiClient.post(`/articles/${id}/like`);
    return response.data;
  },

  unlikeArticle: async (id) => {
    await apiClient.delete(`/articles/${id}/like`);
  },

  getComments: async (id) => {
    const response = await apiClient.get(`/articles/${id}/comments`);
    return response.data;
  },

  createComment: async (id, content) => {
    const response = await apiClient.post(`/articles/${id}/comments`, {
      article_id: id,
      content,
    });
    return response.data;
  },
};

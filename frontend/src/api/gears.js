import apiClient from './client';

export const gearsAPI = {
  getGears: (params) => apiClient.get('/gears', { params }).then(r => r.data),
  getGear: (id) => apiClient.get(`/gears/${id}`).then(r => r.data),
  getRecommended: (gear_type) => apiClient.get('/gears/recommendations', { params: { gear_type } }).then(r => r.data),
  getReviews: (id) => apiClient.get(`/gears/${id}/reviews`).then(r => r.data),
  createReview: (id, data) => apiClient.post(`/gears/${id}/reviews`, data).then(r => r.data),
  updateReview: (reviewId, data) => apiClient.put(`/gears/reviews/${reviewId}`, data).then(r => r.data),
  deleteReview: (reviewId) => apiClient.delete(`/gears/reviews/${reviewId}`),
};

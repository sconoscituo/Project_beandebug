import apiClient from './client';

export const recipesAPI = {
  // 내 레시피
  getMyRecipes: async (params = {}) => {
    const response = await apiClient.get('/recipes/', { params });
    return response.data;
  },

  // 공개 레시피
  getPublicRecipes: async (params = {}) => {
    const response = await apiClient.get('/recipes/public', { params });
    return response.data;
  },

  // 레시피 상세
  getRecipe: async (id) => {
    const response = await apiClient.get(`/recipes/${id}`);
    return response.data;
  },

  // 레시피 생성
  createRecipe: async (recipeData) => {
    const response = await apiClient.post('/recipes/', recipeData);
    return response.data;
  },

  // 레시피 수정
  updateRecipe: async (id, recipeData) => {
    const response = await apiClient.put(`/recipes/${id}`, recipeData);
    return response.data;
  },

  // 레시피 삭제
  deleteRecipe: async (id) => {
    await apiClient.delete(`/recipes/${id}`);
  },

  // 좋아요
  likeRecipe: async (id) => {
    const response = await apiClient.post(`/recipes/${id}/like`);
    return response.data;
  },

  unlikeRecipe: async (id) => {
    await apiClient.delete(`/recipes/${id}/like`);
  },

  // 댓글
  getComments: async (id) => {
    const response = await apiClient.get(`/recipes/${id}/comments`);
    return response.data;
  },

  createComment: async (id, content) => {
    const response = await apiClient.post(`/recipes/${id}/comments`, {
      recipe_id: id,
      content,
    });
    return response.data;
  },
};
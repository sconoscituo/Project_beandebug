import apiClient from './client';

export const recipesAPI = {
  getMyRecipes: async (params = {}) => {
    const response = await apiClient.get('/recipes/', { params });
    return response.data;
  },

  getPublicRecipes: async (params = {}) => {
    const response = await apiClient.get('/recipes/public', { params });
    return response.data;
  },

  getRecipe: async (id) => {
    const response = await apiClient.get(`/recipes/${id}`);
    return response.data;
  },

  createRecipe: async (recipeData) => {
    const response = await apiClient.post('/recipes/', recipeData);
    return response.data;
  },

  updateRecipe: async (id, recipeData) => {
    const response = await apiClient.put(`/recipes/${id}`, recipeData);
    return response.data;
  },

  deleteRecipe: async (id) => {
    await apiClient.delete(`/recipes/${id}`);
  },

  // likes
  likeRecipe: async (id) => {
    const response = await apiClient.post(`/recipes/${id}/like`);
    return response.data;
  },

  unlikeRecipe: async (id) => {
    await apiClient.delete(`/recipes/${id}/like`);
  },

  // comments
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

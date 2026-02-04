import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { recipesAPI } from '../api';

const Recipes = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('recent');

  useEffect(() => {
    loadRecipes();
  }, [sortBy]);

  const loadRecipes = async () => {
    try {
      const data = await recipesAPI.getPublicRecipes({ sort_by: sortBy, limit: 50 });
      setRecipes(data);
    } catch (error) {
      console.error('Failed to load recipes:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-20">Loading...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900">Community Recipes</h1>
        <div className="flex space-x-4">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="input w-48"
          >
            <option value="recent">Most Recent</option>
            <option value="popular">Most Popular</option>
            <option value="rating">Highest Rated</option>
          </select>
          <Link to="/my-recipes/new" className="btn-primary">
            + New Recipe
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {recipes.map((recipe) => (
          <Link
            key={recipe.id}
            to={`/recipes/${recipe.id}`}
            className="card hover:shadow-xl transition-shadow"
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-semibold text-gray-900">
                {recipe.title}
              </h3>
              <span className="bg-coffee-100 text-coffee-700 px-3 py-1 rounded-full text-sm">
                {recipe.brew_method}
              </span>
            </div>
            
            {recipe.description && (
              <p className="text-gray-600 mb-4 line-clamp-2">
                {recipe.description}
              </p>
            )}

            <div className="space-y-2 text-sm text-gray-600 mb-4">
              <div className="flex justify-between">
                <span>Coffee</span>
                <span className="font-medium">{recipe.coffee_amount}g</span>
              </div>
              <div className="flex justify-between">
                <span>Water</span>
                <span className="font-medium">{recipe.water_amount}ml</span>
              </div>
              <div className="flex justify-between">
                <span>Ratio</span>
                <span className="font-medium">{recipe.ratio || '1:16'}</span>
              </div>
            </div>

            <div className="flex justify-between items-center pt-4 border-t text-sm text-gray-500">
              <div className="flex items-center space-x-4">
                <span>❤️ {recipe.likes_count}</span>
                <span>👁️ {recipe.view_count}</span>
              </div>
              {recipe.overall_rating && (
                <span className="text-yellow-600">
                  ⭐ {recipe.overall_rating.toFixed(1)}
                </span>
              )}
            </div>
          </Link>
        ))}
      </div>

      {recipes.length === 0 && (
        <div className="text-center py-20 text-gray-500">
          No recipes found. Be the first to share!
        </div>
      )}
    </div>
  );
};

export default Recipes;
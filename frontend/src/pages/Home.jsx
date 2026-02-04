import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { recipesAPI, articlesAPI } from '../api';

const Home = () => {
  const [featuredRecipes, setFeaturedRecipes] = useState([]);
  const [latestArticles, setLatestArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [recipes, articles] = await Promise.all([
        recipesAPI.getPublicRecipes({ sort_by: 'popular', limit: 6 }),
        articlesAPI.getArticles({ limit: 3, published_only: true }),
      ]);
      setFeaturedRecipes(recipes);
      setLatestArticles(articles);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-2xl text-coffee-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-coffee-50 to-white">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-6xl font-bold text-coffee-800 mb-4">
            Hello World! 👋
          </h1>
          <h2 className="text-3xl text-coffee-600 mb-8">
            Debugging Coffee Bean
          </h2>
          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
            커피 추출을 코드 디버깅하듯이. 완벽한 한 잔을 위한 여정을 시작하세요.
          </p>
          <div className="flex justify-center space-x-4">
            <Link to="/recipes" className="btn-primary text-lg px-8 py-3">
              레시피 탐색하기
            </Link>
            <Link to="/beans" className="btn-secondary text-lg px-8 py-3">
              원두 알아보기
            </Link>
          </div>
        </div>
      </div>

      {/* Popular Recipes */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Popular Recipes</h2>
          <Link to="/recipes" className="text-coffee-600 hover:text-coffee-700">
            View all →
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredRecipes.map((recipe) => (
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
              <p className="text-gray-600 mb-4 line-clamp-2">
                {recipe.description || 'No description'}
              </p>
              <div className="flex justify-between items-center text-sm text-gray-500">
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
      </div>

      {/* Latest Articles */}
      <div className="bg-coffee-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Latest Articles</h2>
            <Link to="/articles" className="text-coffee-600 hover:text-coffee-700">
              View all →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {latestArticles.map((article) => (
              <Link
                key={article.id}
                to={`/articles/${article.id}`}
                className="card hover:shadow-xl transition-shadow"
              >
                <div className="mb-2">
                  <span className="text-xs text-coffee-600 uppercase tracking-wide">
                    {article.category.replace('_', ' ')}
                  </span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {article.title}
                </h3>
                <p className="text-gray-600 text-sm line-clamp-3">
                  {article.summary}
                </p>
                <div className="mt-4 flex items-center justify-between text-sm text-gray-500">
                  <span>👁️ {article.view_count}</span>
                  <span>❤️ {article.likes_count}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Bean of the Month - Placeholder */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="card bg-gradient-to-r from-coffee-100 to-coffee-200">
          <div className="text-center py-12">
            <h2 className="text-3xl font-bold text-coffee-800 mb-4">
              Bean of the Month
            </h2>
            <p className="text-coffee-700 mb-6">
              Coming soon! 매월 엄선된 원두를 소개합니다.
            </p>
            <Link to="/beans" className="btn-primary">
              원두 둘러보기
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
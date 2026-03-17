import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { recipesAPI } from '../api';
import { sampleRecipes } from '../data/sampleData';
import Pagination from '../components/Pagination';

const PAGE_SIZE = 12;

const Recipes = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('recent');
  const [filter, setFilter] = useState('all');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [usingFallback, setUsingFallback] = useState(false);

  const brewMethods = [
    { id: 'all', name: 'All', icon: '☕' },
    { id: 'V60', name: 'V60', icon: '🔻' },
    { id: 'Aeropress', name: 'Aeropress', icon: '💨' },
    { id: 'French Press', name: 'French Press', icon: '🫖' },
    { id: 'Moka Pot', name: 'Moka Pot', icon: '☕' },
    { id: 'Cold Brew', name: 'Cold Brew', icon: '🧊' },
    { id: 'Espresso', name: 'Espresso', icon: '⚡' },
    { id: 'Chemex', name: 'Chemex', icon: '🧪' },
  ];

  useEffect(() => {
    loadRecipes();
  }, [filter, sortBy, page]);

  const loadRecipes = async () => {
    setLoading(true);
    try {
      const params = { sort_by: sortBy, page, page_size: PAGE_SIZE };
      if (filter !== 'all') params.brew_method = filter;
      const data = await recipesAPI.getPublicRecipes(params);
      const items = data.items ?? data;
      if (!Array.isArray(items) || items.length === 0) throw new Error('empty');
      setRecipes(items);
      setTotalPages(data.total_pages ?? 1);
      setUsingFallback(false);
    } catch {
      // Fall back to sample data with client-side filter + sort + pagination
      let filtered = filter === 'all'
        ? sampleRecipes
        : sampleRecipes.filter((r) => r.brew_method === filter);

      if (sortBy === 'popular') {
        filtered = [...filtered].sort((a, b) => (b.likes_count || 0) - (a.likes_count || 0));
      } else if (sortBy === 'rating') {
        filtered = [...filtered].sort((a, b) => (b.overall_rating || 0) - (a.overall_rating || 0));
      }

      const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
      setTotalPages(pages);
      const start = (page - 1) * PAGE_SIZE;
      setRecipes(filtered.slice(start, start + PAGE_SIZE));
      setUsingFallback(true);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (methodId) => {
    setFilter(methodId);
    setPage(1);
  };

  const handleSortChange = (e) => {
    setSortBy(e.target.value);
    setPage(1);
  };

  const handlePageChange = (newPage) => {
    setPage(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
      paddingTop: '120px',
      paddingBottom: '4rem',
    }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 2rem' }}>
        {/* Header */}
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ fontFamily: "'Fira Code', monospace", color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
            <span style={{ color: '#00ff88' }}>$</span> ls ./recipes
          </div>
          <h1 style={{ fontFamily: "'Fira Code', monospace", fontSize: '2.5rem', color: '#00ff88', marginBottom: '0.5rem' }}>
            Brewing Recipes
          </h1>
          <p style={{ color: '#666', fontFamily: "'Fira Code', monospace", fontSize: '0.9rem' }}>
            // 커뮤니티의 다양한 추출 레시피를 탐색하세요
            {usingFallback && (
              <span style={{ color: '#444', marginLeft: '1rem' }}>// [sample data]</span>
            )}
          </p>
        </div>

        {/* Controls */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '2rem',
          flexWrap: 'wrap',
          gap: '1rem',
        }}>
          {/* Filter Tabs */}
          <div style={{
            display: 'flex',
            gap: '0.5rem',
            overflowX: 'auto',
            paddingBottom: '0.5rem',
            WebkitOverflowScrolling: 'touch',
            scrollbarWidth: 'none',
          }}>
            {brewMethods.map((method) => (
              <button
                key={method.id}
                onClick={() => handleFilterChange(method.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  padding: '0.5rem 1rem',
                  background: filter === method.id ? '#00ff88' : '#1e1e1e',
                  color: filter === method.id ? '#0a0a0a' : '#888',
                  border: `1px solid ${filter === method.id ? '#00ff88' : '#333'}`,
                  borderRadius: '6px',
                  fontFamily: "'Fira Code', monospace",
                  fontSize: '0.8rem',
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                  transition: 'all 0.3s ease',
                }}
              >
                <span>{method.icon}</span>
                <span>{method.name}</span>
              </button>
            ))}
          </div>

          {/* Sort & New Button */}
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <select
              value={sortBy}
              onChange={handleSortChange}
              style={{
                padding: '0.5rem 1rem',
                background: '#1e1e1e',
                border: '1px solid #333',
                borderRadius: '6px',
                color: '#888',
                fontFamily: "'Fira Code', monospace",
                fontSize: '0.85rem',
                cursor: 'pointer',
              }}
            >
              <option value="recent">최신순</option>
              <option value="popular">인기순</option>
              <option value="rating">평점순</option>
            </select>
            <Link
              to="/my-recipes/new"
              style={{
                padding: '0.5rem 1.25rem',
                background: '#00ff88',
                color: '#0a0a0a',
                borderRadius: '6px',
                textDecoration: 'none',
                fontFamily: "'Fira Code', monospace",
                fontSize: '0.85rem',
                fontWeight: '600',
                whiteSpace: 'nowrap',
              }}
            >
              + new()
            </Link>
          </div>
        </div>

        {/* Recipe Grid */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '4rem', fontFamily: "'Fira Code', monospace", color: '#00ff88' }}>
            <span className="loading-cursor">Loading recipes...</span>
          </div>
        ) : recipes.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '4rem', fontFamily: "'Fira Code', monospace", color: '#666' }}>
            // No recipes found. Be the first to share!
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '1.5rem',
          }}>
            {recipes.map((recipe) => (
              <Link key={recipe.id} to={`/recipes/${recipe.id}`} style={{ textDecoration: 'none' }}>
                <div
                  style={{
                    background: '#1e1e1e',
                    borderRadius: '12px',
                    border: '1px solid #333',
                    overflow: 'hidden',
                    transition: 'all 0.3s ease',
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.borderColor = '#00ff88';
                    e.currentTarget.style.boxShadow = '0 0 20px rgba(0, 255, 136, 0.2)';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.borderColor = '#333';
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                >
                  {/* Card Header */}
                  <div style={{
                    background: '#2d2d2d',
                    padding: '10px 14px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    borderBottom: '1px solid #333',
                  }}>
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }} />
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }} />
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27ca3f' }} />
                    <span style={{ marginLeft: '8px', color: '#888', fontFamily: "'Fira Code', monospace", fontSize: '0.75rem' }}>
                      {recipe.brew_method?.toLowerCase().replace(/\s+/g, '_') || 'recipe'}.js
                    </span>
                  </div>

                  {/* Card Body */}
                  <div style={{ padding: '1.25rem' }}>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      marginBottom: '1rem',
                      gap: '0.5rem',
                    }}>
                      <h3 style={{ fontFamily: "'Fira Code', monospace", fontSize: '1rem', color: '#00ff88', margin: 0 }}>
                        {recipe.title}
                      </h3>
                      <span style={{
                        padding: '2px 8px',
                        background: 'rgba(0, 255, 136, 0.1)',
                        border: '1px solid rgba(0, 255, 136, 0.3)',
                        borderRadius: '4px',
                        color: '#00ff88',
                        fontFamily: "'Fira Code', monospace",
                        fontSize: '0.7rem',
                        whiteSpace: 'nowrap',
                      }}>
                        {recipe.brew_method}
                      </span>
                    </div>

                    {recipe.description && (
                      <p style={{
                        fontFamily: "'Fira Code', monospace",
                        fontSize: '0.8rem',
                        color: '#666',
                        marginBottom: '1rem',
                        lineHeight: 1.5,
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                      }}>
                        // {recipe.description}
                      </p>
                    )}

                    <div style={{ fontFamily: "'Fira Code', monospace", fontSize: '0.8rem', color: '#ccc', lineHeight: '1.7' }}>
                      <div>
                        <span style={{ color: '#ff79c6' }}>coffee</span>
                        <span style={{ color: '#888' }}>: </span>
                        <span style={{ color: '#f1fa8c' }}>"{recipe.coffee_amount}g"</span>
                      </div>
                      <div>
                        <span style={{ color: '#ff79c6' }}>water</span>
                        <span style={{ color: '#888' }}>: </span>
                        <span style={{ color: '#f1fa8c' }}>"{recipe.water_amount}ml"</span>
                      </div>
                      <div>
                        <span style={{ color: '#ff79c6' }}>ratio</span>
                        <span style={{ color: '#888' }}>: </span>
                        <span style={{ color: '#f1fa8c' }}>"{recipe.ratio || '1:16'}"</span>
                      </div>
                    </div>

                    <div style={{
                      marginTop: '1rem',
                      paddingTop: '1rem',
                      borderTop: '1px solid #333',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.75rem',
                    }}>
                      <div style={{ display: 'flex', gap: '1rem', color: '#666' }}>
                        <span style={{ color: '#ff79c6' }}>♥ {recipe.likes_count || 0}</span>
                        <span style={{ color: '#8be9fd' }}>👁 {recipe.view_count || 0}</span>
                      </div>
                      {recipe.overall_rating && (
                        <span style={{ color: '#f1fa8c' }}>★ {recipe.overall_rating.toFixed(1)}</span>
                      )}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        <Pagination page={page} totalPages={totalPages} onPageChange={handlePageChange} />
      </div>

      <style>{`
        @keyframes blink {
          0%, 50% { opacity: 1; }
          51%, 100% { opacity: 0; }
        }
        .loading-cursor::after {
          content: '|';
          animation: blink 1s infinite;
        }
      `}</style>
    </div>
  );
};

export default Recipes;

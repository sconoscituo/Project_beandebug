import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { recipesAPI } from '../api';

const RecipeDetail = () => {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;

    const loadRecipe = async () => {
      try {
        setError(null);
        const data = await recipesAPI.getRecipe(id);
        if (mounted) setRecipe(data);
      } catch (err) {
        if (mounted) setError(err);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    loadRecipe();
    return () => { mounted = false; };
  }, [id]);

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
        paddingTop: '120px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <span style={{ color: '#00ff88', fontFamily: "'Fira Code', monospace" }}>
          Loading...
        </span>
      </div>
    );
  }

  if (error || !recipe) {
    return (
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
        paddingTop: '120px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '1rem'
      }}>
        <span style={{ color: '#ff5f56', fontFamily: "'Fira Code', monospace", fontSize: '1.2rem' }}>
          ERROR: RECIPE_NOT_FOUND
        </span>
        <Link to="/recipes" style={{ color: '#00ff88', fontFamily: "'Fira Code', monospace", fontSize: '0.85rem' }}>
          ← back to recipes
        </Link>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
      paddingTop: '100px',
      paddingBottom: '4rem'
    }}>
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '0 2rem' }}>

        <Link to="/recipes" style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          color: '#888',
          textDecoration: 'none',
          fontFamily: "'Fira Code', monospace",
          fontSize: '0.85rem',
          marginBottom: '2rem'
        }}>
          ← back to recipes
        </Link>

        <div style={{
          background: '#1e1e1e',
          borderRadius: '12px',
          border: '1px solid #333',
          overflow: 'hidden'
        }}>
          {/* Card Header */}
          <div style={{
            background: '#2d2d2d',
            padding: '12px 16px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            borderBottom: '1px solid #333'
          }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ff5f56' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ffbd2e' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#27ca3f' }}></div>
            <span style={{
              marginLeft: '8px',
              color: '#888',
              fontFamily: "'Fira Code', monospace",
              fontSize: '0.85rem'
            }}>
              {recipe.brew_method?.toLowerCase()}_recipe.js
            </span>
          </div>

          {/* Card Body */}
          <div style={{ padding: '2rem' }}>
            <div style={{ marginBottom: '1.5rem' }}>
              <h1 style={{
                fontFamily: "'Fira Code', monospace",
                fontSize: '1.75rem',
                color: '#00ff88',
                marginBottom: '0.5rem'
              }}>
                {recipe.title}
              </h1>
              <div style={{
                display: 'flex',
                gap: '1rem',
                fontFamily: "'Fira Code', monospace",
                fontSize: '0.8rem',
                color: '#666'
              }}>
                <span>@{recipe.author?.username}</span>
                <span>{recipe.created_at}</span>
                <span style={{ color: '#f1fa8c' }}>★ {recipe.overall_rating}</span>
              </div>
            </div>

            {/* Description */}
            <p style={{
              fontFamily: "'Fira Code', monospace",
              fontSize: '0.9rem',
              color: '#888',
              lineHeight: 1.6,
              marginBottom: '2rem',
              paddingBottom: '1.5rem',
              borderBottom: '1px solid #333'
            }}>
              // {recipe.description}
            </p>

            {/* Recipe Parameters */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '1rem',
              marginBottom: '2rem'
            }}>
              {[
                { label: 'coffee', value: recipe.coffee_amount ? `${recipe.coffee_amount}g` : '-' },
                { label: 'water', value: recipe.water_amount ? `${recipe.water_amount}ml` : '-' },
                { label: 'temp', value: recipe.water_temp ? `${recipe.water_temp}°C` : '-' },
                { label: 'grind', value: recipe.grind_size || '-' },
                { label: 'time', value: recipe.brew_time ? `${recipe.brew_time}s` : '-' },
                { label: 'ratio', value: recipe.ratio || '-' }
              ].map((item, idx) => (
                <div key={idx} style={{
                  background: '#2d2d2d',
                  padding: '1rem',
                  borderRadius: '8px',
                  border: '1px solid #333'
                }}>
                  <div style={{
                    fontFamily: "'Fira Code', monospace",
                    fontSize: '0.75rem',
                    color: '#ff79c6',
                    marginBottom: '0.25rem'
                  }}>
                    {item.label}
                  </div>
                  <div style={{
                    fontFamily: "'Fira Code', monospace",
                    fontSize: '1rem',
                    color: '#f1fa8c'
                  }}>
                    "{item.value}"
                  </div>
                </div>
              ))}
            </div>

            {/* Steps — backend returns string, split by newline */}
            {recipe.steps && (
              <div style={{ marginBottom: '2rem' }}>
                <h3 style={{
                  fontFamily: "'Fira Code', monospace",
                  fontSize: '1rem',
                  color: '#00ff88',
                  marginBottom: '1rem'
                }}>
                  // Steps
                </h3>
                <div style={{
                  fontFamily: "'Fira Code', monospace",
                  fontSize: '0.85rem',
                  color: '#ccc',
                  lineHeight: 2
                }}>
                  {recipe.steps.split('\n').filter(Boolean).map((step, idx) => (
                    <div key={idx}>
                      <span style={{ color: '#bd93f9' }}>{idx + 1}.</span> {step}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Tips */}
            {recipe.tips && (
              <div style={{
                background: 'rgba(0, 255, 136, 0.1)',
                border: '1px solid rgba(0, 255, 136, 0.3)',
                borderRadius: '8px',
                padding: '1rem',
                marginBottom: '2rem'
              }}>
                <span style={{
                  fontFamily: "'Fira Code', monospace",
                  fontSize: '0.85rem',
                  color: '#00ff88'
                }}>
                  Tip: {recipe.tips}
                </span>
              </div>
            )}

            {/* Footer Stats */}
            <div style={{
              display: 'flex',
              gap: '2rem',
              paddingTop: '1.5rem',
              borderTop: '1px solid #333',
              fontFamily: "'Fira Code', monospace",
              fontSize: '0.85rem'
            }}>
              <span style={{ color: '#ff79c6' }}>♥ {recipe.likes_count} likes</span>
              <span style={{ color: '#8be9fd' }}>👁 {recipe.view_count} views</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetail;

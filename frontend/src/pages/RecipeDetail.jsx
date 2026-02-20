import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { recipesAPI } from '../api';

const RecipeDetail = () => {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecipe();
  }, [id]);

  const loadRecipe = async () => {
    try {
      const data = await recipesAPI.getRecipe(id);
      setRecipe(data);
    } catch (error) {
      console.error('Failed to load recipe:', error);
    } finally {
      setLoading(false);
    }
  };

  // 샘플 데이터 (API 연결 전)
  const sampleRecipe = {
    id: 1,
    title: 'V60 기본 레시피',
    brew_method: 'V60',
    description: '깔끔하고 밝은 산미를 즐길 수 있는 기본 V60 추출법입니다. 초보자도 쉽게 따라할 수 있어요.',
    coffee_amount: 18,
    water_amount: 300,
    water_temp: 93,
    grind_size: 'Medium-Fine',
    brew_time: '3:00',
    ratio: '1:16.7',
    steps: [
      '필터를 린싱하고 커피를 담습니다',
      '30g 물로 30초간 블루밍',
      '원을 그리며 천천히 푸어링',
      '2분 30초에 추출 완료'
    ],
    tips: '물줄기를 일정하게 유지하세요',
    likes_count: 124,
    view_count: 1520,
    overall_rating: 4.8,
    author: { username: 'coffee_master' },
    created_at: '2026-02-15'
  };

  const displayRecipe = recipe || sampleRecipe;

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

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
      paddingTop: '100px',
      paddingBottom: '4rem'
    }}>
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '0 2rem' }}>
        
        {/* Back Button */}
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

        {/* Main Card */}
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
              {displayRecipe.brew_method?.toLowerCase()}_recipe.js
            </span>
          </div>

          {/* Card Body */}
          <div style={{ padding: '2rem' }}>
            {/* Title */}
            <div style={{ marginBottom: '1.5rem' }}>
              <h1 style={{
                fontFamily: "'Fira Code', monospace",
                fontSize: '1.75rem',
                color: '#00ff88',
                marginBottom: '0.5rem'
              }}>
                {displayRecipe.title}
              </h1>
              <div style={{
                display: 'flex',
                gap: '1rem',
                fontFamily: "'Fira Code', monospace",
                fontSize: '0.8rem',
                color: '#666'
              }}>
                <span>@{displayRecipe.author?.username}</span>
                <span>{displayRecipe.created_at}</span>
                <span style={{ color: '#f1fa8c' }}>★ {displayRecipe.overall_rating}</span>
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
              // {displayRecipe.description}
            </p>

            {/* Recipe Parameters */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '1rem',
              marginBottom: '2rem'
            }}>
              {[
                { label: 'coffee', value: `${displayRecipe.coffee_amount}g` },
                { label: 'water', value: `${displayRecipe.water_amount}ml` },
                { label: 'temp', value: `${displayRecipe.water_temp}°C` },
                { label: 'grind', value: displayRecipe.grind_size },
                { label: 'time', value: displayRecipe.brew_time },
                { label: 'ratio', value: displayRecipe.ratio }
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

            {/* Steps */}
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
                {displayRecipe.steps?.map((step, idx) => (
                  <div key={idx}>
                    <span style={{ color: '#bd93f9' }}>{idx + 1}.</span> {step}
                  </div>
                ))}
              </div>
            </div>

            {/* Tips */}
            {displayRecipe.tips && (
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
                  💡 Tip: {displayRecipe.tips}
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
              <span style={{ color: '#ff79c6' }}>♥ {displayRecipe.likes_count} likes</span>
              <span style={{ color: '#8be9fd' }}>👁 {displayRecipe.view_count} views</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetail;
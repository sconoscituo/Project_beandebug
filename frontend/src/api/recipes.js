import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { recipesAPI } from '../api';

const Recipes = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const data = await recipesAPI.getPublicRecipes();
        setRecipes(data);
      } catch (error) {
        console.error('Failed to fetch recipes:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchRecipes();
  }, []);

  const brewMethods = [
    { id: 'all', name: 'All', icon: '☕' },
    { id: 'v60', name: 'V60', icon: '🔻' },
    { id: 'aeropress', name: 'Aeropress', icon: '💨' },
    { id: 'french_press', name: 'French Press', icon: '🫖' },
    { id: 'moka_pot', name: 'Moka Pot', icon: '☕' },
    { id: 'cold_brew', name: 'Cold Brew', icon: '🧊' },
  ];

  // 샘플 데이터 (API 연결 전)
  const sampleRecipes = [
    {
      id: 1,
      title: 'V60 기본 레시피',
      brew_method: 'V60',
      coffee_dose: 18,
      water_amount: 300,
      brew_time: '3:00',
      grind_size: 'Medium-Fine',
      water_temp: 93,
      rating: 4.8,
      likes: 124,
      author: 'coffee_master'
    },
    {
      id: 2,
      title: '에어로프레스 인버트',
      brew_method: 'Aeropress',
      coffee_dose: 15,
      water_amount: 200,
      brew_time: '2:00',
      grind_size: 'Fine',
      water_temp: 85,
      rating: 4.7,
      likes: 98,
      author: 'barista_kim'
    },
    {
      id: 3,
      title: '콜드브루 12시간',
      brew_method: 'Cold Brew',
      coffee_dose: 100,
      water_amount: 1000,
      brew_time: '12:00:00',
      grind_size: 'Coarse',
      water_temp: 4,
      rating: 4.9,
      likes: 256,
      author: 'cold_brew_fan'
    },
    {
      id: 4,
      title: '모카포트 에스프레소',
      brew_method: 'Moka Pot',
      coffee_dose: 20,
      water_amount: 150,
      brew_time: '5:00',
      grind_size: 'Fine',
      water_temp: 100,
      rating: 4.6,
      likes: 87,
      author: 'italian_style'
    },
  ];

  const displayRecipes = recipes.length > 0 ? recipes : sampleRecipes;

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
      paddingTop: '120px',
      paddingBottom: '4rem'
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '0 2rem'
      }}>
        {/* Header */}
        <div style={{
          marginBottom: '3rem'
        }}>
          <div style={{
            fontFamily: "'Fira Code', monospace",
            color: '#888',
            fontSize: '0.9rem',
            marginBottom: '0.5rem'
          }}>
            <span style={{ color: '#00ff88' }}>$</span> ls ./recipes
          </div>
          <h1 style={{
            fontFamily: "'Fira Code', monospace",
            fontSize: '2.5rem',
            color: '#00ff88',
            marginBottom: '0.5rem'
          }}>
            Brewing Recipes
          </h1>
          <p style={{
            color: '#666',
            fontFamily: "'Fira Code', monospace",
            fontSize: '0.9rem'
          }}>
            // 커뮤니티의 다양한 추출 레시피를 탐색하세요
          </p>
        </div>

        {/* Filter Tabs */}
        <div style={{
          display: 'flex',
          gap: '0.75rem',
          marginBottom: '2rem',
          overflowX: 'auto',
          paddingBottom: '0.5rem',
          WebkitOverflowScrolling: 'touch',
          scrollbarWidth: 'none'
        }}>
          {brewMethods.map((method) => (
            <button
              key={method.id}
              onClick={() => setFilter(method.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.6rem 1.2rem',
                background: filter === method.id ? '#00ff88' : '#1e1e1e',
                color: filter === method.id ? '#0a0a0a' : '#888',
                border: `1px solid ${filter === method.id ? '#00ff88' : '#333'}`,
                borderRadius: '6px',
                fontFamily: "'Fira Code', monospace",
                fontSize: '0.85rem',
                cursor: 'pointer',
                whiteSpace: 'nowrap',
                transition: 'all 0.3s ease'
              }}
            >
              <span>{method.icon}</span>
              <span>{method.name}</span>
            </button>
          ))}
        </div>

        {/* Recipe Grid */}
        {loading ? (
          <div style={{
            textAlign: 'center',
            padding: '4rem',
            fontFamily: "'Fira Code', monospace",
            color: '#00ff88'
          }}>
            <span className="loading-cursor">Loading recipes...</span>
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
            gap: '1.5rem'
          }}>
            {displayRecipes.map((recipe) => (
              <Link
                key={recipe.id}
                to={`/recipes/${recipe.id}`}
                style={{
                  textDecoration: 'none'
                }}
              >
                <div style={{
                  background: '#1e1e1e',
                  borderRadius: '12px',
                  border: '1px solid #333',
                  overflow: 'hidden',
                  transition: 'all 0.3s ease'
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
                    padding: '12px 16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    borderBottom: '1px solid #333'
                  }}>
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }}></div>
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }}></div>
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27ca3f' }}></div>
                    <span style={{
                      marginLeft: '8px',
                      color: '#888',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.8rem'
                    }}>
                      {recipe.brew_method.toLowerCase()}.recipe
                    </span>
                  </div>

                  {/* Card Body */}
                  <div style={{ padding: '1.5rem' }}>
                    {/* Title */}
                    <h3 style={{
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '1.1rem',
                      color: '#00ff88',
                      marginBottom: '1rem'
                    }}>
                      {recipe.title}
                    </h3>

                    {/* Recipe Details */}
                    <div style={{
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.85rem',
                      color: '#ccc',
                      lineHeight: '1.8'
                    }}>
                      <div>
                        <span style={{ color: '#ff79c6' }}>const</span>
                        <span style={{ color: '#f8f8f2' }}> coffee</span>
                        <span style={{ color: '#ff79c6' }}> = </span>
                        <span style={{ color: '#f1fa8c' }}>"{recipe.coffee_dose}g"</span>
                        <span style={{ color: '#888' }}>;</span>
                      </div>
                      <div>
                        <span style={{ color: '#ff79c6' }}>const</span>
                        <span style={{ color: '#f8f8f2' }}> water</span>
                        <span style={{ color: '#ff79c6' }}> = </span>
                        <span style={{ color: '#f1fa8c' }}>"{recipe.water_amount}ml"</span>
                        <span style={{ color: '#888' }}>;</span>
                      </div>
                      <div>
                        <span style={{ color: '#ff79c6' }}>const</span>
                        <span style={{ color: '#f8f8f2' }}> temp</span>
                        <span style={{ color: '#ff79c6' }}> = </span>
                        <span style={{ color: '#bd93f9' }}>{recipe.water_temp}</span>
                        <span style={{ color: '#888' }}>; // °C</span>
                      </div>
                      <div>
                        <span style={{ color: '#ff79c6' }}>const</span>
                        <span style={{ color: '#f8f8f2' }}> time</span>
                        <span style={{ color: '#ff79c6' }}> = </span>
                        <span style={{ color: '#f1fa8c' }}>"{recipe.brew_time}"</span>
                        <span style={{ color: '#888' }}>;</span>
                      </div>
                      <div>
                        <span style={{ color: '#ff79c6' }}>const</span>
                        <span style={{ color: '#f8f8f2' }}> grind</span>
                        <span style={{ color: '#ff79c6' }}> = </span>
                        <span style={{ color: '#f1fa8c' }}>"{recipe.grind_size}"</span>
                        <span style={{ color: '#888' }}>;</span>
                      </div>
                    </div>

                    {/* Footer */}
                    <div style={{
                      marginTop: '1.5rem',
                      paddingTop: '1rem',
                      borderTop: '1px solid #333',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.8rem'
                    }}>
                      <span style={{ color: '#666' }}>
                        @{recipe.author}
                      </span>
                      <div style={{ display: 'flex', gap: '1rem' }}>
                        <span style={{ color: '#ff79c6' }}>
                          ♥ {recipe.likes}
                        </span>
                        <span style={{ color: '#f1fa8c' }}>
                          ★ {recipe.rating}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Create Recipe Button */}
        <div style={{
          textAlign: 'center',
          marginTop: '3rem'
        }}>
          <Link
            to="/recipes/create"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '1rem 2rem',
              background: '#00ff88',
              color: '#0a0a0a',
              borderRadius: '8px',
              textDecoration: 'none',
              fontFamily: "'Fira Code', monospace",
              fontWeight: '600',
              transition: 'all 0.3s ease'
            }}
            onMouseOver={(e) => {
              e.target.style.boxShadow = '0 0 30px rgba(0, 255, 136, 0.4)';
            }}
            onMouseOut={(e) => {
              e.target.style.boxShadow = 'none';
            }}
          >
            + createRecipe()
          </Link>
        </div>
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
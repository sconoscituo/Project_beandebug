import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { beansAPI } from '../api';

const Beans = () => {
  const [beans, setBeans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchBeans = async () => {
      try {
        const data = await beansAPI.getPublicBeans();
        setBeans(data);
      } catch (error) {
        console.error('Failed to fetch beans:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchBeans();
  }, []);

  const origins = [
    { id: 'all', name: 'All', icon: '🌍' },
    { id: 'ethiopia', name: 'Ethiopia', icon: '🇪🇹' },
    { id: 'colombia', name: 'Colombia', icon: '🇨🇴' },
    { id: 'brazil', name: 'Brazil', icon: '🇧🇷' },
    { id: 'kenya', name: 'Kenya', icon: '🇰🇪' },
    { id: 'guatemala', name: 'Guatemala', icon: '🇬🇹' },
  ];

  const roastLevels = {
    light: { color: '#f1fa8c', label: 'Light' },
    medium: { color: '#ffb86c', label: 'Medium' },
    medium_dark: { color: '#ff79c6', label: 'Med-Dark' },
    dark: { color: '#bd93f9', label: 'Dark' }
  };

  // 샘플 데이터 (API 연결 전)
  const sampleBeans = [
    {
      id: 1,
      name: '예가체프 코체레',
      origin: 'Ethiopia',
      region: 'Yirgacheffe',
      roast_level: 'light',
      process: 'Washed',
      flavor_notes: ['Floral', 'Citrus', 'Tea-like'],
      altitude: '1,800-2,200m',
      rating: 4.9,
      roaster: 'Coffee Lab'
    },
    {
      id: 2,
      name: '콜롬비아 수프리모',
      origin: 'Colombia',
      region: 'Huila',
      roast_level: 'medium',
      process: 'Washed',
      flavor_notes: ['Chocolate', 'Caramel', 'Nutty'],
      altitude: '1,500-1,800m',
      rating: 4.7,
      roaster: 'Bean Bros'
    },
    {
      id: 3,
      name: '케냐 AA',
      origin: 'Kenya',
      region: 'Nyeri',
      roast_level: 'light',
      process: 'Washed',
      flavor_notes: ['Blackcurrant', 'Grapefruit', 'Wine'],
      altitude: '1,700-2,000m',
      rating: 4.8,
      roaster: 'Artisan Roasters'
    },
    {
      id: 4,
      name: '브라질 산토스',
      origin: 'Brazil',
      region: 'Minas Gerais',
      roast_level: 'medium_dark',
      process: 'Natural',
      flavor_notes: ['Nuts', 'Chocolate', 'Low Acid'],
      altitude: '1,000-1,300m',
      rating: 4.5,
      roaster: 'Daily Roast'
    },
    {
      id: 5,
      name: '과테말라 안티구아',
      origin: 'Guatemala',
      region: 'Antigua',
      roast_level: 'medium',
      process: 'Washed',
      flavor_notes: ['Cocoa', 'Spice', 'Smoky'],
      altitude: '1,500-1,700m',
      rating: 4.6,
      roaster: 'Mountain Coffee'
    },
  ];

  const displayBeans = beans.length > 0 ? beans : sampleBeans;

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
            <span style={{ color: '#00ff88' }}>$</span> cat ./beans/collection.json
          </div>
          <h1 style={{
            fontFamily: "'Fira Code', monospace",
            fontSize: '2.5rem',
            color: '#00ff88',
            marginBottom: '0.5rem'
          }}>
            Coffee Beans
          </h1>
          <p style={{
            color: '#666',
            fontFamily: "'Fira Code', monospace",
            fontSize: '0.9rem'
          }}>
            // 전 세계의 스페셜티 원두를 탐색하세요
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
          {origins.map((origin) => (
            <button
              key={origin.id}
              onClick={() => setFilter(origin.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.6rem 1.2rem',
                background: filter === origin.id ? '#00ff88' : '#1e1e1e',
                color: filter === origin.id ? '#0a0a0a' : '#888',
                border: `1px solid ${filter === origin.id ? '#00ff88' : '#333'}`,
                borderRadius: '6px',
                fontFamily: "'Fira Code', monospace",
                fontSize: '0.85rem',
                cursor: 'pointer',
                whiteSpace: 'nowrap',
                transition: 'all 0.3s ease'
              }}
            >
              <span>{origin.icon}</span>
              <span>{origin.name}</span>
            </button>
          ))}
        </div>

        {/* Beans Grid */}
        {loading ? (
          <div style={{
            textAlign: 'center',
            padding: '4rem',
            fontFamily: "'Fira Code', monospace",
            color: '#00ff88'
          }}>
            <span className="loading-cursor">Fetching beans...</span>
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
            gap: '1.5rem'
          }}>
            {displayBeans.map((bean) => (
              <Link
                key={bean.id}
                to={`/beans/${bean.id}`}
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
                    justifyContent: 'space-between',
                    borderBottom: '1px solid #333'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }}></div>
                      <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }}></div>
                      <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27ca3f' }}></div>
                      <span style={{
                        marginLeft: '8px',
                        color: '#888',
                        fontFamily: "'Fira Code', monospace",
                        fontSize: '0.8rem'
                      }}>
                        {bean.origin.toLowerCase()}.bean
                      </span>
                    </div>
                    {/* Roast Level Badge */}
                    <span style={{
                      padding: '2px 8px',
                      background: roastLevels[bean.roast_level]?.color || '#888',
                      color: '#0a0a0a',
                      borderRadius: '4px',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.7rem',
                      fontWeight: '600'
                    }}>
                      {roastLevels[bean.roast_level]?.label || bean.roast_level}
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
                      {bean.name}
                    </h3>

                    {/* Bean Details */}
                    <div style={{
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.85rem',
                      color: '#ccc',
                      lineHeight: '1.8'
                    }}>
                      <div>
                        <span style={{ color: '#ff79c6' }}>origin</span>
                        <span style={{ color: '#888' }}>: </span>
                        <span style={{ color: '#f1fa8c' }}>"{bean.origin}"</span>
                        <span style={{ color: '#888' }}>,</span>
                      </div>
                      <div>
                        <span style={{ color: '#ff79c6' }}>region</span>
                        <span style={{ color: '#888' }}>: </span>
                        <span style={{ color: '#f1fa8c' }}>"{bean.region}"</span>
                        <span style={{ color: '#888' }}>,</span>
                      </div>
                      <div>
                        <span style={{ color: '#ff79c6' }}>process</span>
                        <span style={{ color: '#888' }}>: </span>
                        <span style={{ color: '#f1fa8c' }}>"{bean.process}"</span>
                        <span style={{ color: '#888' }}>,</span>
                      </div>
                      <div>
                        <span style={{ color: '#ff79c6' }}>altitude</span>
                        <span style={{ color: '#888' }}>: </span>
                        <span style={{ color: '#f1fa8c' }}>"{bean.altitude}"</span>
                        <span style={{ color: '#888' }}>,</span>
                      </div>
                    </div>

                    {/* Flavor Notes */}
                    <div style={{
                      marginTop: '1rem',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.85rem'
                    }}>
                      <span style={{ color: '#ff79c6' }}>flavors</span>
                      <span style={{ color: '#888' }}>: [</span>
                      <div style={{
                        display: 'flex',
                        flexWrap: 'wrap',
                        gap: '0.5rem',
                        marginTop: '0.5rem',
                        marginLeft: '1rem'
                      }}>
                        {bean.flavor_notes.map((note, index) => (
                          <span key={index} style={{
                            padding: '2px 8px',
                            background: 'rgba(0, 255, 136, 0.1)',
                            border: '1px solid rgba(0, 255, 136, 0.3)',
                            borderRadius: '4px',
                            color: '#00ff88',
                            fontSize: '0.75rem'
                          }}>
                            "{note}"
                          </span>
                        ))}
                      </div>
                      <span style={{ color: '#888', marginLeft: '0' }}>]</span>
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
                        roaster: {bean.roaster}
                      </span>
                      <span style={{ color: '#f1fa8c' }}>
                        ★ {bean.rating}
                      </span>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Add Bean Button */}
        <div style={{
          textAlign: 'center',
          marginTop: '3rem'
        }}>
          <Link
            to="/beans/create"
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
            + addBean()
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

export default Beans;
import React, { useEffect, useState } from 'react';
import { gearsAPI } from '../api';

const GEAR_TYPE_LABELS = {
  grinder: 'Grinder',
  brewer: 'Brewer',
  espresso_machine: 'Espresso Machine',
  kettle: 'Kettle',
  scale: 'Scale',
  filter: 'Filter',
  accessories: 'Accessories',
};

const Gears = () => {
  const [gears, setGears] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [recommendedOnly, setRecommendedOnly] = useState(false);

  useEffect(() => {
    loadGears();
  }, [filter, recommendedOnly]);

  const loadGears = async () => {
    setLoading(true);
    try {
      const params = { limit: 100 };
      if (filter) params.gear_type = filter;
      if (recommendedOnly) params.recommended_only = true;
      const data = await gearsAPI.getGears(params);
      setGears(data);
    } catch (error) {
      console.error('Failed to load gears:', error);
    } finally {
      setLoading(false);
    }
  };

  const gearTypes = [{ id: '', name: 'All' }, ...Object.entries(GEAR_TYPE_LABELS).map(([id, name]) => ({ id, name }))];

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
      paddingTop: '120px',
      paddingBottom: '4rem'
    }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 2rem' }}>
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ fontFamily: "'Fira Code', monospace", color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
            <span style={{ color: '#00ff88' }}>$</span> ls ./gears
          </div>
          <h1 style={{ fontFamily: "'Fira Code', monospace", fontSize: '2.5rem', color: '#00ff88', marginBottom: '0.5rem' }}>
            Coffee Gear
          </h1>
          <p style={{ color: '#666', fontFamily: "'Fira Code', monospace", fontSize: '0.9rem' }}>
            // 커피 장비를 탐색하고 리뷰를 확인하세요
          </p>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', gap: '0.5rem', overflowX: 'auto', paddingBottom: '0.5rem' }}>
            {gearTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => setFilter(type.id)}
                style={{
                  padding: '0.5rem 1rem',
                  background: filter === type.id ? '#00ff88' : '#1e1e1e',
                  color: filter === type.id ? '#0a0a0a' : '#888',
                  border: `1px solid ${filter === type.id ? '#00ff88' : '#333'}`,
                  borderRadius: '6px',
                  fontFamily: "'Fira Code', monospace",
                  fontSize: '0.8rem',
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                  transition: 'all 0.3s ease'
                }}
              >
                {type.name}
              </button>
            ))}
          </div>
          <button
            onClick={() => setRecommendedOnly(prev => !prev)}
            style={{
              padding: '0.5rem 1.25rem',
              background: recommendedOnly ? '#f1fa8c' : '#1e1e1e',
              color: recommendedOnly ? '#0a0a0a' : '#888',
              border: `1px solid ${recommendedOnly ? '#f1fa8c' : '#333'}`,
              borderRadius: '6px',
              fontFamily: "'Fira Code', monospace",
              fontSize: '0.8rem',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            ★ recommended
          </button>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '4rem', fontFamily: "'Fira Code', monospace", color: '#00ff88' }}>
            <span>Loading gears...</span>
          </div>
        ) : gears.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '4rem', fontFamily: "'Fira Code', monospace", color: '#666' }}>
            // No gear found.
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
            {gears.map((gear) => (
              <div
                key={gear.id}
                style={{
                  background: '#1e1e1e',
                  borderRadius: '12px',
                  border: '1px solid #333',
                  overflow: 'hidden',
                  transition: 'all 0.3s ease'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.borderColor = '#00ff88';
                  e.currentTarget.style.boxShadow = '0 0 20px rgba(0,255,136,0.2)';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.borderColor = '#333';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <div style={{ background: '#2d2d2d', padding: '10px 14px', display: 'flex', alignItems: 'center', gap: '8px', borderBottom: '1px solid #333' }}>
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }} />
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }} />
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27ca3f' }} />
                  <span style={{ marginLeft: '8px', color: '#888', fontFamily: "'Fira Code', monospace", fontSize: '0.75rem' }}>
                    {GEAR_TYPE_LABELS[gear.gear_type] || gear.gear_type}.gear
                  </span>
                  {gear.is_recommended && (
                    <span style={{ marginLeft: 'auto', color: '#f1fa8c', fontSize: '0.7rem', fontFamily: "'Fira Code', monospace" }}>★ rec</span>
                  )}
                </div>

                {gear.image_url && (
                  <img
                    src={gear.image_url}
                    alt={gear.name}
                    style={{ width: '100%', height: '160px', objectFit: 'cover' }}
                    onError={(e) => { e.currentTarget.style.display = 'none'; }}
                  />
                )}

                <div style={{ padding: '1.25rem' }}>
                  <h3 style={{ fontFamily: "'Fira Code', monospace", fontSize: '1rem', color: '#00ff88', margin: '0 0 0.25rem 0' }}>
                    {gear.name}
                  </h3>
                  {gear.brand && (
                    <p style={{ fontFamily: "'Fira Code', monospace", fontSize: '0.8rem', color: '#888', margin: '0 0 0.75rem 0' }}>
                      {gear.brand} {gear.model && `/ ${gear.model}`}
                    </p>
                  )}
                  {gear.description && (
                    <p style={{
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.78rem',
                      color: '#666',
                      marginBottom: '1rem',
                      lineHeight: 1.5,
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical'
                    }}>
                      {gear.description}
                    </p>
                  )}

                  <div style={{ fontFamily: "'Fira Code', monospace", fontSize: '0.8rem', color: '#ccc', lineHeight: '1.7' }}>
                    {(gear.price_min || gear.price_max) && (
                      <div>
                        <span style={{ color: '#ff79c6' }}>price</span>
                        <span style={{ color: '#888' }}>: </span>
                        <span style={{ color: '#f1fa8c' }}>
                          {gear.currency} {gear.price_min && gear.price_max
                            ? `${gear.price_min} ~ ${gear.price_max}`
                            : gear.price_min || gear.price_max}
                        </span>
                      </div>
                    )}
                  </div>

                  <div style={{
                    marginTop: '1rem',
                    paddingTop: '1rem',
                    borderTop: '1px solid #333',
                    display: 'flex',
                    justifyContent: 'space-between',
                    fontFamily: "'Fira Code', monospace",
                    fontSize: '0.75rem'
                  }}>
                    <span style={{ color: '#f1fa8c' }}>
                      ★ {gear.average_rating > 0 ? gear.average_rating.toFixed(1) : 'N/A'}
                    </span>
                    <span style={{ color: '#8be9fd' }}>
                      {gear.review_count} review{gear.review_count !== 1 ? 's' : ''}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Gears;

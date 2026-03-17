import React, { useEffect, useState } from 'react';
import { gearsAPI } from '../api';
import { sampleGears } from '../data/sampleData';
import Pagination from '../components/Pagination';

const PAGE_SIZE = 12;

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
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [usingFallback, setUsingFallback] = useState(false);

  const gearTypes = [
    { id: '', name: 'All' },
    ...Object.entries(GEAR_TYPE_LABELS).map(([id, name]) => ({ id, name })),
  ];

  useEffect(() => {
    loadGears();
  }, [filter, recommendedOnly, page]);

  const loadGears = async () => {
    setLoading(true);
    try {
      const params = { page, page_size: PAGE_SIZE };
      if (filter) params.gear_type = filter;
      if (recommendedOnly) params.recommended_only = true;
      const data = await gearsAPI.getGears(params);
      const items = data.items ?? data;
      if (!Array.isArray(items) || items.length === 0) throw new Error('empty');
      setGears(items);
      setTotalPages(data.total_pages ?? 1);
      setUsingFallback(false);
    } catch {
      // Fall back to sample data with client-side filter + pagination
      let filtered = sampleGears;
      if (filter) filtered = filtered.filter((g) => g.gear_type === filter);
      if (recommendedOnly) filtered = filtered.filter((g) => g.is_recommended);
      const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
      setTotalPages(pages);
      const start = (page - 1) * PAGE_SIZE;
      setGears(filtered.slice(start, start + PAGE_SIZE));
      setUsingFallback(true);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (typeId) => {
    setFilter(typeId);
    setPage(1);
  };

  const handleRecommendedToggle = () => {
    setRecommendedOnly((prev) => !prev);
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
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ fontFamily: "'Fira Code', monospace", color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
            <span style={{ color: '#00ff88' }}>$</span> ls ./gears
          </div>
          <h1 style={{ fontFamily: "'Fira Code', monospace", fontSize: '2.5rem', color: '#00ff88', marginBottom: '0.5rem' }}>
            Coffee Gear
          </h1>
          <p style={{ color: '#666', fontFamily: "'Fira Code', monospace", fontSize: '0.9rem' }}>
            // 커피 장비를 탐색하고 리뷰를 확인하세요
            {usingFallback && (
              <span style={{ color: '#444', marginLeft: '1rem' }}>// [sample data]</span>
            )}
          </p>
        </div>

        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '2rem',
          flexWrap: 'wrap',
          gap: '1rem',
        }}>
          <div style={{
            display: 'flex',
            gap: '0.5rem',
            overflowX: 'auto',
            paddingBottom: '0.5rem',
            WebkitOverflowScrolling: 'touch',
            scrollbarWidth: 'none',
          }}>
            {gearTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => handleFilterChange(type.id)}
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
                  transition: 'all 0.3s ease',
                }}
              >
                {type.name}
              </button>
            ))}
          </div>
          <button
            onClick={handleRecommendedToggle}
            style={{
              padding: '0.5rem 1.25rem',
              background: recommendedOnly ? '#f1fa8c' : '#1e1e1e',
              color: recommendedOnly ? '#0a0a0a' : '#888',
              border: `1px solid ${recommendedOnly ? '#f1fa8c' : '#333'}`,
              borderRadius: '6px',
              fontFamily: "'Fira Code', monospace",
              fontSize: '0.8rem',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
            }}
          >
            ★ recommended
          </button>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '4rem', fontFamily: "'Fira Code', monospace", color: '#00ff88' }}>
            <span className="loading-cursor">Loading gears...</span>
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
                  transition: 'all 0.3s ease',
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
                    {GEAR_TYPE_LABELS[gear.gear_type] || gear.gear_type}.gear
                  </span>
                  {gear.is_recommended && (
                    <span style={{ marginLeft: 'auto', color: '#f1fa8c', fontSize: '0.7rem', fontFamily: "'Fira Code', monospace" }}>
                      ★ rec
                    </span>
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
                      {gear.brand}{gear.model && ` / ${gear.model}`}
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
                      WebkitBoxOrient: 'vertical',
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
                          {gear.currency}{' '}
                          {gear.price_min && gear.price_max
                            ? `${gear.price_min.toLocaleString()} ~ ${gear.price_max.toLocaleString()}`
                            : (gear.price_min || gear.price_max).toLocaleString()}
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
                    fontSize: '0.75rem',
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

export default Gears;

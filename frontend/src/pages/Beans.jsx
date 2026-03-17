import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { sampleBeans } from '../data/sampleData';
import Pagination from '../components/Pagination';

const PAGE_SIZE = 12;

const Beans = () => {
  const [beans, setBeans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [usingFallback, setUsingFallback] = useState(false);

  const origins = [
    { id: 'all', name: 'All', icon: '🌍' },
    { id: 'Ethiopia', name: 'Ethiopia', icon: '🇪🇹' },
    { id: 'Colombia', name: 'Colombia', icon: '🇨🇴' },
    { id: 'Brazil', name: 'Brazil', icon: '🇧🇷' },
    { id: 'Kenya', name: 'Kenya', icon: '🇰🇪' },
    { id: 'Panama', name: 'Panama', icon: '🇵🇦' },
    { id: 'Guatemala', name: 'Guatemala', icon: '🇬🇹' },
    { id: 'Costa Rica', name: 'Costa Rica', icon: '🇨🇷' },
    { id: 'Rwanda', name: 'Rwanda', icon: '🇷🇼' },
    { id: 'Indonesia', name: 'Indonesia', icon: '🇮🇩' },
    { id: 'Jamaica', name: 'Jamaica', icon: '🇯🇲' },
  ];

  const roastColors = {
    light: '#f1fa8c',
    medium: '#ffb86c',
    medium_dark: '#ff79c6',
    dark: '#bd93f9',
  };

  useEffect(() => {
    loadBeans();
  }, [filter, page]);

  const loadBeans = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page, page_size: PAGE_SIZE });
      if (filter !== 'all') params.append('origin', filter);
      const response = await fetch(`/api/beans/public?${params}`);
      if (!response.ok) throw new Error('API error');
      const data = await response.json();
      const items = data.items ?? data;
      if (!Array.isArray(items) || items.length === 0) throw new Error('empty');
      setBeans(items);
      setTotalPages(data.total_pages ?? 1);
      setUsingFallback(false);
    } catch {
      // Fall back to sample data with client-side filter + pagination
      const filtered = filter === 'all'
        ? sampleBeans
        : sampleBeans.filter((b) => b.origin === filter);
      const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
      setTotalPages(pages);
      const start = (page - 1) * PAGE_SIZE;
      setBeans(filtered.slice(start, start + PAGE_SIZE));
      setUsingFallback(true);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (originId) => {
    setFilter(originId);
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
            <span style={{ color: '#00ff88' }}>$</span> cat ./beans/collection.json
          </div>
          <h1 style={{ fontFamily: "'Fira Code', monospace", fontSize: '2.5rem', color: '#00ff88', marginBottom: '0.5rem' }}>
            Coffee Beans
          </h1>
          <p style={{ color: '#666', fontFamily: "'Fira Code', monospace", fontSize: '0.9rem' }}>
            // 전 세계의 스페셜티 원두를 탐색하세요
            {usingFallback && (
              <span style={{ color: '#444', marginLeft: '1rem' }}>// [sample data]</span>
            )}
          </p>
        </div>

        {/* Filter */}
        <div style={{
          display: 'flex',
          gap: '0.5rem',
          marginBottom: '2rem',
          overflowX: 'auto',
          paddingBottom: '0.5rem',
          WebkitOverflowScrolling: 'touch',
          scrollbarWidth: 'none',
        }}>
          {origins.map((origin) => (
            <button
              key={origin.id}
              onClick={() => handleFilterChange(origin.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                padding: '0.5rem 1rem',
                background: filter === origin.id ? '#00ff88' : '#1e1e1e',
                color: filter === origin.id ? '#0a0a0a' : '#888',
                border: `1px solid ${filter === origin.id ? '#00ff88' : '#333'}`,
                borderRadius: '6px',
                fontFamily: "'Fira Code', monospace",
                fontSize: '0.8rem',
                cursor: 'pointer',
                whiteSpace: 'nowrap',
                transition: 'all 0.2s ease',
              }}
            >
              <span>{origin.icon}</span>
              <span>{origin.name}</span>
            </button>
          ))}
        </div>

        {/* Grid */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '4rem', fontFamily: "'Fira Code', monospace", color: '#00ff88' }}>
            <span className="loading-cursor">Loading beans...</span>
          </div>
        ) : beans.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '4rem', fontFamily: "'Fira Code', monospace", color: '#666' }}>
            // No beans found.
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1.5rem' }}>
            {beans.map((bean) => (
              <Link key={bean.id} to={`/beans/${bean.id}`} style={{ textDecoration: 'none' }}>
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
                    justifyContent: 'space-between',
                    borderBottom: '1px solid #333',
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }} />
                      <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }} />
                      <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27ca3f' }} />
                      <span style={{ marginLeft: '8px', color: '#888', fontFamily: "'Fira Code', monospace", fontSize: '0.75rem' }}>
                        {bean.origin.toLowerCase()}.bean
                      </span>
                    </div>
                    <span style={{
                      padding: '2px 8px',
                      background: roastColors[bean.roast_level] || '#888',
                      color: '#0a0a0a',
                      borderRadius: '4px',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.65rem',
                      fontWeight: '600',
                    }}>
                      {bean.roast_level}
                    </span>
                  </div>

                  {/* Card Body */}
                  <div style={{ padding: '1.25rem' }}>
                    <h3 style={{ fontFamily: "'Fira Code', monospace", fontSize: '1rem', color: '#00ff88', marginBottom: '1rem' }}>
                      {bean.name}
                    </h3>
                    <div style={{ fontFamily: "'Fira Code', monospace", fontSize: '0.8rem', color: '#ccc', lineHeight: '1.7' }}>
                      <div><span style={{ color: '#ff79c6' }}>origin</span>: <span style={{ color: '#f1fa8c' }}>"{bean.origin}"</span></div>
                      <div><span style={{ color: '#ff79c6' }}>region</span>: <span style={{ color: '#f1fa8c' }}>"{bean.region}"</span></div>
                      <div><span style={{ color: '#ff79c6' }}>process</span>: <span style={{ color: '#f1fa8c' }}>"{bean.process}"</span></div>
                      <div><span style={{ color: '#ff79c6' }}>altitude</span>: <span style={{ color: '#f1fa8c' }}>"{bean.altitude}"</span></div>
                    </div>

                    {/* Flavor Notes */}
                    <div style={{ marginTop: '1rem', display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                      {(bean.flavor_notes || []).map((note, idx) => (
                        <span key={idx} style={{
                          padding: '2px 8px',
                          background: 'rgba(0, 255, 136, 0.1)',
                          border: '1px solid rgba(0, 255, 136, 0.3)',
                          borderRadius: '4px',
                          color: '#00ff88',
                          fontFamily: "'Fira Code', monospace",
                          fontSize: '0.7rem',
                        }}>
                          {note}
                        </span>
                      ))}
                    </div>

                    {/* Footer */}
                    <div style={{
                      marginTop: '1rem',
                      paddingTop: '1rem',
                      borderTop: '1px solid #333',
                      display: 'flex',
                      justifyContent: 'space-between',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.75rem',
                    }}>
                      <span style={{ color: '#666' }}>{bean.roaster}</span>
                      <span style={{ color: '#f1fa8c' }}>★ {bean.rating}</span>
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

export default Beans;

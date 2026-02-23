import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Articles = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  const categories = [
    { id: 'all', name: 'ALL_FILES', icon: '📁' },
    { id: 'new_tech', name: 'NEW_TECH', icon: '📡' },
    { id: 'brewing_guide', name: 'GUIDE', icon: '📖' },
    { id: 'bean_review', name: 'BEAN_REV', icon: '☕' },
    { id: 'gear_review', name: 'GEAR_REV', icon: '🛠️' },
  ];

  const categoryColors = {
    new_tech: '#8be9fd',
    brewing_guide: '#00ff88',
    bean_review: '#f1fa8c',
    gear_review: '#ffb86c',
    general: '#bd93f9'
  };

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        setLoading(true);
        const url = filter === 'all' 
          ? `http://localhost:8000/api/articles/` 
          : `http://localhost:8000/api/articles/?category=${filter}`;
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('DB_ACCESS_DENIED');
        const data = await response.json();
        setArticles(data);
      } catch (error) {
        console.error("System Error:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchArticles();
  }, [filter]);

  return (
    <div style={{ minHeight: '100vh', background: '#0a0a0a', paddingTop: '120px', paddingBottom: '4rem', color: '#ccc', fontFamily: "'Fira Code', monospace" }}>
      <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '0 2rem' }}>
        
        <header style={{ marginBottom: '2rem' }}>
          <div style={{ color: '#00ff88', fontSize: '0.9rem' }}>{"$ query --database=articles --status=published"}</div>
          <h1 style={{ fontSize: '2.5rem', color: '#00ff88', marginTop: '0.5rem', fontWeight: 'bold' }}>INTELLIGENCE_REPORTS</h1>
        </header>

        <div style={{ display: 'flex', gap: '10px', marginBottom: '2rem', overflowX: 'auto', paddingBottom: '10px' }}>
          {categories.map(cat => (
            <button key={cat.id} onClick={() => setFilter(cat.id)} style={{
              padding: '8px 16px', background: filter === cat.id ? '#00ff88' : '#1a1a1a',
              color: filter === cat.id ? '#000' : '#888', border: '1px solid #333',
              borderRadius: '4px', cursor: 'pointer', fontFamily: "'Fira Code', monospace",
              transition: '0.2s'
            }}>
              {`${cat.icon} ${cat.name}`}
            </button>
          ))}
        </div>

        {loading ? (
          <div style={{ color: '#00ff88' }}>{"> ACCESSING_SECURE_SERVER..."}</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
            {articles.length === 0 ? (
              <div style={{ padding: '2rem', border: '1px dashed #444', textAlign: 'center', color: '#666' }}>
                {"NO_REPORTS_FOUND_IN_THIS_SECTION"}
              </div>
            ) : (
              articles.map(article => (
                <Link key={article.id} to={`/articles/${article.id}`} style={{ textDecoration: 'none' }}>
                  <div style={{ background: '#111', border: '1px solid #333', borderRadius: '8px', overflow: 'hidden' }}>
                    <div style={{ background: '#222', padding: '8px 15px', display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #333' }}>
                      <span style={{ fontSize: '0.7rem', color: '#666' }}>{`UID: ${article.id} | SLUG: ${article.slug || 'N/A'}`}</span>
                      <span style={{ 
                        fontSize: '0.65rem', padding: '2px 8px', 
                        background: categoryColors[article.category] || '#444', 
                        color: '#000', borderRadius: '3px', fontWeight: 'bold' 
                      }}>
                        {article.category?.toUpperCase()}
                      </span>
                    </div>
                    <div style={{ display: 'flex', padding: '1.5rem', gap: '1.5rem', flexWrap: 'wrap' }}>
                      <div style={{ width: '180px', height: '110px', background: '#000', border: '1px solid #222', overflow: 'hidden' }}>
                        <img 
                          src={article.thumbnail_url || 'https://via.placeholder.com/180x110?text=ENCRYPTED'} 
                          alt="thumb" 
                          style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: 0.6 }} 
                        />
                      </div>
                      <div style={{ flex: 1, minWidth: '300px' }}>
                        <h3 style={{ color: '#00ff88', marginBottom: '10px', fontSize: '1.2rem' }}>
                          {`> ${article.title}`}
                        </h3>
                        <p style={{ fontSize: '0.9rem', color: '#999', lineHeight: '1.5', marginBottom: '15px' }}>
                          {article.summary || "데이터 요약 정보가 없습니다."}
                        </p>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#555' }}>
                          <span>{`BY: ${article.author_id || 'UNKNOWN_AGENT'}`}</span>
                          <span style={{ color: '#00ff88' }}>{"[ VIEW_REPORT ]"}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </Link>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Articles;
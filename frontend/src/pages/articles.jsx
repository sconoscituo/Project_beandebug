import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Articles = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    setLoading(false);
  }, []);

  const categories = [
    { id: 'all', name: 'All', icon: '📁' },
    { id: 'guide', name: 'Guide', icon: '📖' },
    { id: 'review', name: 'Review', icon: '⭐' },
    { id: 'news', name: 'News', icon: '📰' },
    { id: 'tips', name: 'Tips', icon: '💡' },
  ];

  const sampleArticles = [
    {
      id: 1,
      title: '2024 스페셜티 커피 트렌드 총정리',
      category: 'news',
      summary: '올해 주목해야 할 커피 트렌드와 새로운 브루잉 방법들을 소개합니다.',
      author: 'coffee_editor',
      created_at: '2024-02-15',
      read_time: 8,
      likes: 234
    },
    {
      id: 2,
      title: '홈카페 그라인더 선택 가이드',
      category: 'guide',
      summary: '입문자부터 전문가까지, 예산별 추천 그라인더와 선택 기준을 알아봅니다.',
      author: 'gear_master',
      created_at: '2024-02-12',
      read_time: 12,
      likes: 189
    },
    {
      id: 3,
      title: 'V60 vs 칼리타: 어떤 드리퍼가 맞을까?',
      category: 'review',
      summary: '두 인기 드리퍼의 특성과 맛 차이를 비교 분석했습니다.',
      author: 'brew_scientist',
      created_at: '2024-02-10',
      read_time: 10,
      likes: 156
    },
  ];

  const displayArticles = articles.length > 0 ? articles : sampleArticles;

  const categoryColors = {
    guide: '#00ff88',
    review: '#f1fa8c',
    news: '#8be9fd',
    tips: '#ffb86c'
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
      paddingTop: '120px',
      paddingBottom: '4rem'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 2rem' }}>
        {/* Header */}
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ fontFamily: "'Fira Code', monospace", color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
            <span style={{ color: '#00ff88' }}>$</span> cat ./articles/index.md
          </div>
          <h1 style={{ fontFamily: "'Fira Code', monospace", fontSize: '2.5rem', color: '#00ff88', marginBottom: '0.5rem' }}>
            Articles
          </h1>
          <p style={{ color: '#666', fontFamily: "'Fira Code', monospace", fontSize: '0.9rem' }}>
            // 커피에 관한 가이드, 리뷰, 팁을 읽어보세요
          </p>
        </div>

        {/* Filter */}
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '2rem', overflowX: 'auto', paddingBottom: '0.5rem' }}>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setFilter(cat.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                padding: '0.5rem 1rem',
                background: filter === cat.id ? '#00ff88' : '#1e1e1e',
                color: filter === cat.id ? '#0a0a0a' : '#888',
                border: `1px solid ${filter === cat.id ? '#00ff88' : '#333'}`,
                borderRadius: '6px',
                fontFamily: "'Fira Code', monospace",
                fontSize: '0.8rem',
                cursor: 'pointer',
                whiteSpace: 'nowrap'
              }}
            >
              <span>{cat.icon}</span>
              <span>{cat.name}</span>
            </button>
          ))}
        </div>

        {/* List */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '4rem', fontFamily: "'Fira Code', monospace", color: '#00ff88' }}>
            Loading...
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {displayArticles.map((article) => (
              <Link key={article.id} to={`/articles/${article.id}`} style={{ textDecoration: 'none' }}>
                <div
                  style={{
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
                  {/* Header */}
                  <div style={{
                    background: '#2d2d2d',
                    padding: '10px 14px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    borderBottom: '1px solid #333'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }}></div>
                      <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }}></div>
                      <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27ca3f' }}></div>
                      <span style={{ marginLeft: '8px', color: '#888', fontFamily: "'Fira Code', monospace", fontSize: '0.75rem' }}>
                        article_{article.id}.md
                      </span>
                    </div>
                    <span style={{
                      padding: '2px 10px',
                      background: categoryColors[article.category] || '#888',
                      color: '#0a0a0a',
                      borderRadius: '4px',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.65rem',
                      fontWeight: '600',
                      textTransform: 'uppercase'
                    }}>
                      {article.category}
                    </span>
                  </div>

                  {/* Body */}
                  <div style={{ padding: '1.25rem' }}>
                    <h3 style={{ fontFamily: "'Fira Code', monospace", fontSize: '1.1rem', color: '#00ff88', marginBottom: '0.5rem' }}>
                      {article.title}
                    </h3>
                    <p style={{ fontFamily: "'Fira Code', monospace", fontSize: '0.85rem', color: '#666', marginBottom: '1rem' }}>
                      // {article.summary}
                    </p>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.75rem',
                      color: '#666'
                    }}>
                      <div style={{ display: 'flex', gap: '1rem' }}>
                        <span><span style={{ color: '#ff79c6' }}>@</span>{article.author}</span>
                        <span>📅 {article.created_at}</span>
                        <span>⏱ {article.read_time}min</span>
                      </div>
                      <span style={{ color: '#ff79c6' }}>♥ {article.likes}</span>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Articles;
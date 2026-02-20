import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { articlesAPI } from '../api';

const Articles = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const data = await articlesAPI.getArticles();
        setArticles(data);
      } catch (error) {
        console.error('Failed to fetch articles:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchArticles();
  }, []);

  const categories = [
    { id: 'all', name: 'All', icon: '📁' },
    { id: 'guide', name: 'Guide', icon: '📖' },
    { id: 'review', name: 'Review', icon: '⭐' },
    { id: 'news', name: 'News', icon: '📰' },
    { id: 'tips', name: 'Tips', icon: '💡' },
    { id: 'story', name: 'Story', icon: '📝' },
  ];

  // 샘플 데이터 (API 연결 전)
  const sampleArticles = [
    {
      id: 1,
      title: '2026 스페셜티 커피 트렌드 총정리',
      category: 'news',
      summary: '올해 주목해야 할 커피 트렌드와 새로운 브루잉 방법들을 소개합니다.',
      author: 'coffee_editor',
      created_at: '2026-02-15',
      read_time: 8,
      likes: 234,
      comments_count: 45
    },
    {
      id: 2,
      title: '홈카페 그라인더 선택 가이드',
      category: 'guide',
      summary: '입문자부터 전문가까지, 예산별 추천 그라인더와 선택 기준을 알아봅니다.',
      author: 'gear_master',
      created_at: '2026-02-12',
      read_time: 12,
      likes: 189,
      comments_count: 67
    },
    {
      id: 3,
      title: 'V60 vs 칼리타: 어떤 드리퍼가 맞을까?',
      category: 'review',
      summary: '두 인기 드리퍼의 특성과 맛 차이를 비교 분석했습니다.',
      author: 'brew_scientist',
      created_at: '2026-02-10',
      read_time: 10,
      likes: 156,
      comments_count: 38
    },
    {
      id: 4,
      title: '에티오피아 vs 케냐: 아프리카 원두 비교',
      category: 'review',
      summary: '아프리카 대표 산지 두 곳의 원두 특성과 맛 프로파일을 비교합니다.',
      author: 'bean_explorer',
      created_at: '2026-02-08',
      read_time: 7,
      likes: 198,
      comments_count: 52
    },
    {
      id: 5,
      title: '커피 추출의 과학: 물 온도의 비밀',
      category: 'tips',
      summary: '물 온도가 커피 맛에 미치는 영향과 최적의 온도를 찾는 방법.',
      author: 'coffee_scientist',
      created_at: '2026-02-05',
      read_time: 6,
      likes: 145,
      comments_count: 29
    },
    {
      id: 6,
      title: '나의 바리스타 도전기',
      category: 'story',
      summary: '평범한 직장인이 바리스타 자격증을 따기까지의 여정을 공유합니다.',
      author: 'coffee_dreamer',
      created_at: '2026-02-01',
      read_time: 15,
      likes: 312,
      comments_count: 89
    },
  ];

  const displayArticles = articles.length > 0 ? articles : sampleArticles;

  const getCategoryIcon = (category) => {
    const found = categories.find(c => c.id === category);
    return found ? found.icon : '📄';
  };

  const getCategoryColor = (category) => {
    const colors = {
      guide: '#00ff88',
      review: '#f1fa8c',
      news: '#8be9fd',
      tips: '#ffb86c',
      story: '#ff79c6'
    };
    return colors[category] || '#888';
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
      paddingTop: '120px',
      paddingBottom: '4rem'
    }}>
      <div style={{
        maxWidth: '1200px',
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
            <span style={{ color: '#00ff88' }}>$</span> cat ./articles/index.md
          </div>
          <h1 style={{
            fontFamily: "'Fira Code', monospace",
            fontSize: '2.5rem',
            color: '#00ff88',
            marginBottom: '0.5rem'
          }}>
            Articles
          </h1>
          <p style={{
            color: '#666',
            fontFamily: "'Fira Code', monospace",
            fontSize: '0.9rem'
          }}>
            // 커피에 관한 가이드, 리뷰, 팁을 읽어보세요
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
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setFilter(category.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.6rem 1.2rem',
                background: filter === category.id ? '#00ff88' : '#1e1e1e',
                color: filter === category.id ? '#0a0a0a' : '#888',
                border: `1px solid ${filter === category.id ? '#00ff88' : '#333'}`,
                borderRadius: '6px',
                fontFamily: "'Fira Code', monospace",
                fontSize: '0.85rem',
                cursor: 'pointer',
                whiteSpace: 'nowrap',
                transition: 'all 0.3s ease'
              }}
            >
              <span>{category.icon}</span>
              <span>{category.name}</span>
            </button>
          ))}
        </div>

        {/* Articles List */}
        {loading ? (
          <div style={{
            textAlign: 'center',
            padding: '4rem',
            fontFamily: "'Fira Code', monospace",
            color: '#00ff88'
          }}>
            <span className="loading-cursor">Loading articles...</span>
          </div>
        ) : (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
          }}>
            {displayArticles.map((article) => (
              <Link
                key={article.id}
                to={`/articles/${article.id}`}
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
                    padding: '10px 16px',
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
                        article_{article.id}.md
                      </span>
                    </div>
                    <span style={{
                      padding: '2px 10px',
                      background: getCategoryColor(article.category),
                      color: '#0a0a0a',
                      borderRadius: '4px',
                      fontFamily: "'Fira Code', monospace",
                      fontSize: '0.7rem',
                      fontWeight: '600',
                      textTransform: 'uppercase'
                    }}>
                      {getCategoryIcon(article.category)} {article.category}
                    </span>
                  </div>

                  {/* Card Body */}
                  <div style={{ padding: '1.5rem' }}>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      gap: '2rem'
                    }}>
                      {/* Content */}
                      <div style={{ flex: 1 }}>
                        {/* Title */}
                        <h3 style={{
                          fontFamily: "'Fira Code', monospace",
                          fontSize: '1.2rem',
                          color: '#00ff88',
                          marginBottom: '0.75rem',
                          lineHeight: 1.4
                        }}>
                          {article.title}
                        </h3>

                        {/* Summary */}
                        <p style={{
                          fontFamily: "'Fira Code', monospace",
                          fontSize: '0.9rem',
                          color: '#888',
                          lineHeight: 1.6,
                          marginBottom: '1rem'
                        }}>
                          <span style={{ color: '#666' }}>// </span>
                          {article.summary}
                        </p>

                        {/* Meta Info */}
                        <div style={{
                          display: 'flex',
                          gap: '1.5rem',
                          fontFamily: "'Fira Code', monospace",
                          fontSize: '0.8rem',
                          color: '#666',
                          flexWrap: 'wrap'
                        }}>
                          <span>
                            <span style={{ color: '#ff79c6' }}>@</span>
                            {article.author}
                          </span>
                          <span>
                            <span style={{ color: '#8be9fd' }}>📅</span> {article.created_at}
                          </span>
                          <span>
                            <span style={{ color: '#f1fa8c' }}>⏱</span> {article.read_time} min read
                          </span>
                        </div>
                      </div>

                      {/* Stats */}
                      <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '0.5rem',
                        fontFamily: "'Fira Code', monospace",
                        fontSize: '0.85rem',
                        textAlign: 'right'
                      }}>
                        <span style={{ color: '#ff79c6' }}>
                          ♥ {article.likes}
                        </span>
                        <span style={{ color: '#8be9fd' }}>
                          💬 {article.comments_count}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Write Article Button */}
        <div style={{
          textAlign: 'center',
          marginTop: '3rem'
        }}>
          <Link
            to="/articles/create"
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
            + writeArticle()
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

export default Articles;
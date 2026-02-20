import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const timer = requestAnimationFrame(() => {
      setIsLoaded(true);
    });
    
    return () => cancelAnimationFrame(timer);
  }, []);

  const popularRecipes = [
    {
      id: 1,
      title: 'V60 기본 레시피',
      description: '깔끔하고 밝은 산미를 즐길 수 있는 기본 V60 추출법',
      image: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400',
      method: 'V60',
      time: '3분',
      rating: 4.8
    },
    {
      id: 2,
      title: '에어로프레스 인버트',
      description: '풍부한 바디감과 깊은 풍미의 인버트 방식',
      image: 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400',
      method: 'Aeropress',
      time: '2분',
      rating: 4.7
    },
    {
      id: 3,
      title: '콜드브루 12시간',
      description: '부드럽고 달콤한 콜드브루 레시피',
      image: 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400',
      method: 'Cold Brew',
      time: '12시간',
      rating: 4.9
    },
    {
      id: 4,
      title: '모카포트 에스프레소',
      description: '집에서 즐기는 진한 에스프레소 스타일',
      image: 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400',
      method: 'Moka Pot',
      time: '5분',
      rating: 4.6
    }
  ];

  const latestArticles = [
    {
      id: 1,
      title: '2026 스페셜티 커피 트렌드',
      category: 'TREND',
      image: 'https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=400',
      date: '2026.02.04'
    },
    {
      id: 2,
      title: '홈카페 그라인더 선택 가이드',
      category: 'GEAR',
      image: 'https://images.unsplash.com/photo-1587734195503-904fca47e0e9?w=400',
      date: '2026.02.03'
    },
    {
      id: 3,
      title: '에티오피아 vs 케냐 원두 비교',
      category: 'BEAN',
      image: 'https://images.unsplash.com/photo-1559525839-b184a4d698c7?w=400',
      date: '2026.02.02'
    }
  ];

  return (
    <div style={{ paddingTop: '70px' }}>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text" style={{
            opacity: isLoaded ? 1 : 0,
            transform: isLoaded ? 'translateY(0)' : 'translateY(30px)',
            transition: 'all 0.8s ease'
          }}>
            <h1>
              완벽한 한 잔을<br />
              <span style={{ 
                color: '#00ff88', 
                fontFamily: "'Fira Code', monospace",
              }}>
                {'<debug />'}
              </span>
              하다
            </h1>
            <p>
              모두를 위한 커피 분석 플랫폼<br />
              완벽한 한 잔을 위하여 ☺️
            </p>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'flex-start' }}>
              <Link to="/recipes" className="btn-primary">
                레시피 탐색하기 →
              </Link>
              <Link to="/register" className="btn-secondary">
                시작하기
              </Link>
            </div>
          </div>
          
        </div>
      </section>

      {/* Popular Recipes Section */}
      <section className="section">
        <div className="section-header">
          <h2 className="section-title">인기 레시피</h2>
          <Link to="/recipes" className="section-link">
            전체보기 →
          </Link>
        </div>
        <div className="card-grid">
          {popularRecipes.map((recipe, index) => (
            <Link 
              key={recipe.id}
              to={`/recipes/${recipe.id}`} 
              className="card"
              style={{
                opacity: isLoaded ? 1 : 0,
                transform: isLoaded ? 'translateY(0)' : 'translateY(30px)',
                transition: `all 0.6s ease ${index * 0.1}s`
              }}
            >
              <img 
                src={recipe.image} 
                alt={recipe.title}
                className="card-image"
              />
              <div className="card-content">
                <span className="card-tag">{recipe.method}</span>
                <h3 className="card-title">{recipe.title}</h3>
                <p className="card-description">{recipe.description}</p>
                <div className="card-meta">
                  <span>⏱️ {recipe.time}</span>
                  <span>⭐ {recipe.rating}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Section - Bean of the Month */}
      <section className="featured-section">
        <div className="featured-content">
          <div className="featured-text">
            <span className="featured-label">Bean of the Month</span>
            <h2 className="featured-title">
              에티오피아<br />
              예가체프 코체레
            </h2>
            <p className="featured-description">
              꽃향과 시트러스, 그리고 홍차를 연상시키는 우아한 풍미.<br />
              이번 달 추천 원두로 새로운 커피 경험을 시작하세요.
            </p>
            <Link to="/beans" className="btn-primary">
              원두 살펴보기 →
            </Link>
          </div>
          <div className="featured-image">
            <img 
              src="https://images.unsplash.com/photo-1559525839-b184a4d698c7?w=600" 
              alt="Featured Bean"
            />
          </div>
        </div>
      </section>

      {/* Latest Articles Section */}
      <section className="section">
        <div className="section-header">
          <h2 className="section-title">Recent Article</h2>
          <Link to="/articles" className="section-link">
            전체보기 →
          </Link>
        </div>
        <div className="card-grid">
          {latestArticles.map((article, index) => (
            <Link 
              key={article.id}
              to={`/articles/${article.id}`} 
              className="card"
              style={{
                opacity: isLoaded ? 1 : 0,
                transform: isLoaded ? 'translateY(0)' : 'translateY(30px)',
                transition: `all 0.6s ease ${index * 0.1}s`
              }}
            >
              <img 
                src={article.image} 
                alt={article.title}
                className="card-image"
              />
              <div className="card-content">
                <span className="card-tag">{article.category}</span>
                <h3 className="card-title">{article.title}</h3>
                <div className="card-meta">
                  <span>{article.date}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section style={{
        background: 'linear-gradient(135deg, #f5f1eb 0%, #e8e0d5 100%)',
        padding: '5rem 2rem',
        textAlign: 'center'
      }}>
        <h2 style={{
          fontFamily: "'Playfair Display', serif",
          fontSize: '2.5rem',
          color: '#2C1810',
          marginBottom: '1rem'
        }}>
          나만의 커피 여정을 시작하세요
        </h2>
        <p style={{
          color: '#666',
          fontSize: '1.1rem',
          marginBottom: '2rem',
          maxWidth: '600px',
          margin: '0 auto 2rem'
        }}>
          추출 기록, 레시피 공유, 커뮤니티까지.<br />
          Bean Debug와 함께 완벽한 한 잔을 찾아보세요.
        </p>
        <Link to="/register" className="btn-primary" style={{
          background: '#2C1810',
          color: '#ffffff'
        }}>
          무료로 시작하기 →
        </Link>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div>
            <div className="footer-logo">Bean Debug</div>
            <p className="footer-description">
              커피 추출의 모든 것을 기록하고<br />
              분석하는 플랫폼
            </p>
          </div>
          <div>
            <h4 className="footer-title">서비스</h4>
            <ul className="footer-links">
              <li><Link to="/recipes">Recipes</Link></li>
              <li><Link to="/beans">Beans</Link></li>
              <li><Link to="/gears">Gear</Link></li>
              <li><Link to="/articles">Article</Link></li>  
            </ul>
          </div>
          <div>
            <h4 className="footer-title">Community</h4>
            <ul className="footer-links">
              <li><Link to="/community">커뮤니티</Link></li>
              <li><Link to="/guides">브루잉 가이드</Link></li>
              <li><a href="#">FAQ</a></li>
            </ul>
          </div>
          <div>
            <h4 className="footer-title">문의</h4>
            <ul className="footer-links">
              <li><a href="mailto:hello@beandebug.com">hello@beandebug.com</a></li>
              <li><a href="#">Instagram</a></li>
              <li><a href="#">GitHub</a></li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          © 2026 Bean Debug. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default Home;
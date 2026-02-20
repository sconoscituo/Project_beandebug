import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const categories = [
    { name: 'Beans', link: '/beans' },
    { name: 'Recipes', link: '/recipes' },
    { name: 'Articles', link: '/articles' },
    { name: 'Gears', link: '/gears' },
    { name: 'Community', link: '/community' },
  ];

  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      background: 'rgba(26, 26, 26, 0.95)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
    }}>
      {/* Top Bar */}
      <div style={{
        background: '#D4A574',
        color: '#1a1a1a',
        textAlign: 'center',
        padding: '0.5rem',
        fontSize: '0.85rem',
        fontWeight: '500'
      }}>
        ☕ 다양한 레시피를 위한 커피 디버깅 커뮤니티입니다. 🌟
      </div>

      {/* Main Nav */}
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '1rem 2rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        {/* Logo */}
        <Link to="/" style={{
          fontFamily: "'Playfair Display', serif",
          fontSize: '1.75rem',
          fontWeight: '700',
          color: '#ffffff',
          textDecoration: 'none',
          letterSpacing: '-0.5px',
          flexShrink: 0
        }}>
          Bean Debug
        </Link>

        {/* Desktop Menu - 드래그 가능 */}
        <div className="nav-menu" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1.5rem',
          overflowX: 'auto',
          WebkitOverflowScrolling: 'touch',
          scrollbarWidth: 'none',
          msOverflowStyle: 'none',
          flex: 1,
          justifyContent: 'center',
          padding: '0 1rem'
        }}>
          {categories.map((cat, index) => (
            <Link 
              key={index}
              to={cat.link} 
              style={{
                ...navLinkStyle,
                whiteSpace: 'nowrap',
                flexShrink: 0
              }}
            >
              {cat.name}
            </Link>
          ))}
        </div>

        {/* Mobile Menu Button */}
        <button
          className="mobile-menu-btn"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          style={{
            display: 'none',
            background: 'transparent',
            border: 'none',
            color: '#ffffff',
            fontSize: '1.5rem',
            cursor: 'pointer',
            padding: '0.5rem'
          }}
        >
          {isMenuOpen ? '✕' : '☰'}
        </button>

        {/* Auth Buttons - 드래그 가능 */}
        <div className="auth-buttons" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          flexShrink: 0
        }}>
          {user ? (
            <>
              <span style={{
                color: 'rgba(255, 255, 255, 0.8)',
                fontSize: '0.9rem',
                whiteSpace: 'nowrap'
              }}>
                {user.username}님
              </span>
              <Link to="/my-recipes" style={{
                color: '#D4A574',
                textDecoration: 'none',
                fontSize: '0.9rem',
                fontWeight: '500',
                whiteSpace: 'nowrap'
              }}>
                내 레시피
              </Link>
              <button
                onClick={handleLogout}
                style={{
                  background: 'transparent',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  color: '#ffffff',
                  padding: '0.5rem 1.25rem',
                  borderRadius: '25px',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  transition: 'all 0.3s ease',
                  whiteSpace: 'nowrap'
                }}
                onMouseOver={(e) => {
                  e.target.style.borderColor = '#ffffff';
                  e.target.style.background = 'rgba(255, 255, 255, 0.1)';
                }}
                onMouseOut={(e) => {
                  e.target.style.borderColor = 'rgba(255, 255, 255, 0.3)';
                  e.target.style.background = 'transparent';
                }}
              >
                로그아웃
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={{
                color: 'rgba(255, 255, 255, 0.9)',
                textDecoration: 'none',
                fontSize: '0.9rem',
                fontWeight: '500',
                whiteSpace: 'nowrap'
              }}>
                로그인
              </Link>
              <Link to="/register" style={{
                background: '#D4A574',
                color: '#1a1a1a',
                padding: '0.6rem 1.5rem',
                borderRadius: '25px',
                textDecoration: 'none',
                fontSize: '0.9rem',
                fontWeight: '600',
                transition: 'all 0.3s ease',
                whiteSpace: 'nowrap'
              }}>
                회원가입
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {isMenuOpen && (
        <div style={{
          background: 'rgba(26, 26, 26, 0.98)',
          padding: '1rem 2rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          {categories.map((cat, index) => (
            <Link 
              key={index}
              to={cat.link} 
              onClick={() => setIsMenuOpen(false)}
              style={{
                color: 'rgba(255, 255, 255, 0.85)',
                textDecoration: 'none',
                fontSize: '1rem',
                fontWeight: '500',
                padding: '0.5rem 0'
              }}
            >
              {cat.name}
            </Link>
          ))}
          <div style={{ 
            borderTop: '1px solid rgba(255, 255, 255, 0.1)', 
            paddingTop: '1rem',
            display: 'flex',
            gap: '1rem'
          }}>
            {user ? (
              <button
                onClick={() => {
                  handleLogout();
                  setIsMenuOpen(false);
                }}
                style={{
                  background: 'transparent',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  color: '#ffffff',
                  padding: '0.5rem 1.25rem',
                  borderRadius: '25px',
                  cursor: 'pointer',
                  fontSize: '0.9rem'
                }}
              >
                로그아웃
              </button>
            ) : (
              <>
                <Link 
                  to="/login" 
                  onClick={() => setIsMenuOpen(false)}
                  style={{
                    color: 'rgba(255, 255, 255, 0.9)',
                    textDecoration: 'none',
                    fontSize: '0.9rem',
                    fontWeight: '500'
                  }}
                >
                  로그인
                </Link>
                <Link 
                  to="/register" 
                  onClick={() => setIsMenuOpen(false)}
                  style={{
                    background: '#D4A574',
                    color: '#1a1a1a',
                    padding: '0.6rem 1.5rem',
                    borderRadius: '25px',
                    textDecoration: 'none',
                    fontSize: '0.9rem',
                    fontWeight: '600'
                  }}
                >
                  회원가입
                </Link>
              </>
            )}
          </div>
        </div>
      )}

      <style>{`
        .nav-menu::-webkit-scrollbar {
          display: none;
        }
        
        @media (max-width: 768px) {
          .nav-menu {
            display: none !important;
          }
          
          .auth-buttons {
            display: none !important;
          }
          
          .mobile-menu-btn {
            display: block !important;
          }
        }
      `}</style>
    </nav>
  );
};

const navLinkStyle = {
  color: 'rgba(255, 255, 255, 0.85)',
  textDecoration: 'none',
  fontSize: '0.95rem',
  fontWeight: '500',
  transition: 'color 0.3s ease',
  position: 'relative'
};

export default Navbar;
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
    { name: '☕ Beans', link: '/beans' },
    { name: '📃 Recipes', link: '/recipes' },
    { name: '📰 Articles', link: '/articles' },
    { name: '🦾 Gears', link: '/gears' },
    { name: '💬 Community', link: '/community' },
  ];

  const categoryStyle = {
    color: 'rgba(255, 255, 255, 0.8)',
    textDecoration: 'none',
    fontSize: '0.9rem',
    fontWeight: '500',
    fontFamily: "'Fira Code', monospace",
    padding: '0.5rem 0',
    borderBottom: '2px solid transparent',
    transition: 'all 0.3s ease',
    whiteSpace: 'nowrap',
    flexShrink: 0
  };

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
          fontFamily: "'Fira Code', monospace",
          fontSize: '1.5rem',
          fontWeight: '700',
          color: '#ffffff',
          textDecoration: 'none',
          letterSpacing: '-0.5px',
          flexShrink: 0
        }}>
          {'{ BeanDebug }'}
        </Link>

        {/* Desktop Menu */}
        <div className="nav-menu" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '2rem',
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
              style={categoryStyle}
              onMouseOver={(e) => {
                e.target.style.color = '#ffffff';
                e.target.style.borderBottom = '2px solid #00ff88';
              }}
              onMouseOut={(e) => {
                e.target.style.color = 'rgba(255, 255, 255, 0.8)';
                e.target.style.borderBottom = '2px solid transparent';
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

        {/* Auth Buttons */}
        <div className="auth-buttons" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          flexShrink: 0
        }}>
          {user ? (
            <>
              <span style={{
                color: '#00ff88',
                fontSize: '0.85rem',
                fontFamily: "'Fira Code', monospace",
                whiteSpace: 'nowrap'
              }}>
                @{user.username}
              </span>
              <Link to="/my-recipes" style={{
                color: '#f1fa8c',
                textDecoration: 'none',
                fontSize: '0.85rem',
                fontFamily: "'Fira Code', monospace",
                fontWeight: '500',
                whiteSpace: 'nowrap'
              }}>
                myRecipes()
              </Link>
              <button
                onClick={handleLogout}
                style={{
                  background: 'transparent',
                  border: '1px solid #ff5555',
                  color: '#ff5555',
                  padding: '0.5rem 1rem',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '0.85rem',
                  fontFamily: "'Fira Code', monospace",
                  transition: 'all 0.3s ease',
                  whiteSpace: 'nowrap'
                }}
                onMouseOver={(e) => {
                  e.target.style.background = '#ff5555';
                  e.target.style.color = '#0a0a0a';
                }}
                onMouseOut={(e) => {
                  e.target.style.background = 'transparent';
                  e.target.style.color = '#ff5555';
                }}
              >
                logout()
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={{
                color: '#8be9fd',
                textDecoration: 'none',
                fontSize: '0.85rem',
                fontFamily: "'Fira Code', monospace",
                fontWeight: '500',
                whiteSpace: 'nowrap',
                padding: '0.5rem 1rem',
                border: '1px solid #8be9fd',
                borderRadius: '6px',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => {
                e.target.style.background = '#8be9fd';
                e.target.style.color = '#0a0a0a';
              }}
              onMouseOut={(e) => {
                e.target.style.background = 'transparent';
                e.target.style.color = '#8be9fd';
              }}
              >
                login()
              </Link>
              <Link to="/register" style={{
                background: '#00ff88',
                color: '#0a0a0a',
                padding: '0.5rem 1rem',
                borderRadius: '6px',
                textDecoration: 'none',
                fontSize: '0.85rem',
                fontFamily: "'Fira Code', monospace",
                fontWeight: '600',
                transition: 'all 0.3s ease',
                whiteSpace: 'nowrap'
              }}
              onMouseOver={(e) => {
                e.target.style.boxShadow = '0 0 15px rgba(0, 255, 136, 0.4)';
              }}
              onMouseOut={(e) => {
                e.target.style.boxShadow = 'none';
              }}
              >
                register()
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {isMenuOpen && (
        <div style={{
          background: 'rgba(10, 10, 10, 0.98)',
          padding: '1rem 2rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.5rem',
          borderTop: '1px solid #333'
        }}>
          {categories.map((cat, index) => (
            <Link 
              key={index}
              to={cat.link} 
              onClick={() => setIsMenuOpen(false)}
              style={{
                color: 'rgba(255, 255, 255, 0.8)',
                textDecoration: 'none',
                fontSize: '0.9rem',
                fontFamily: "'Fira Code', monospace",
                fontWeight: '500',
                padding: '0.75rem 0',
                borderBottom: '1px solid #333'
              }}
            >
              {cat.name}
            </Link>
          ))}
          <div style={{ 
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
                  border: '1px solid #ff5555',
                  color: '#ff5555',
                  padding: '0.5rem 1rem',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '0.85rem',
                  fontFamily: "'Fira Code', monospace"
                }}
              >
                logout()
              </button>
            ) : (
              <>
                <Link 
                  to="/login" 
                  onClick={() => setIsMenuOpen(false)}
                  style={{
                    color: '#8be9fd',
                    textDecoration: 'none',
                    fontSize: '0.85rem',
                    fontFamily: "'Fira Code', monospace",
                    fontWeight: '500',
                    padding: '0.5rem 1rem',
                    border: '1px solid #8be9fd',
                    borderRadius: '6px'
                  }}
                >
                  login()
                </Link>
                <Link 
                  to="/register" 
                  onClick={() => setIsMenuOpen(false)}
                  style={{
                    background: '#00ff88',
                    color: '#0a0a0a',
                    padding: '0.5rem 1rem',
                    borderRadius: '6px',
                    textDecoration: 'none',
                    fontSize: '0.85rem',
                    fontFamily: "'Fira Code', monospace",
                    fontWeight: '600'
                  }}
                >
                  register()
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

export default Navbar;
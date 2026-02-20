import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  // eslint-disable-next-line no-unused-vars
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
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
      {/* Top Bar */}
      <div style={{
        background: '#D4A574',
        color: '#1a1a1a',
        textAlign: 'center',
        padding: '0.5rem',
        fontSize: '0.85rem',
        fontWeight: '500'
      }}>
        ☕ 다양한 레시피를 위한 커피 디버깅 커뮤니티입니다.  🌟
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
          letterSpacing: '-0.5px'
        }}>
          Bean Debug
        </Link>

        {/* Desktop Menu */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '2.5rem'
        }}>
          <Link to="/beans" style={navLinkStyle}>원두</Link>
          <Link to="/recipes" style={navLinkStyle}>레시피</Link>
          <Link to="/articles" style={navLinkStyle}>아티클</Link>
          <Link to="/gears" style={navLinkStyle}>장비</Link>
          <Link to="/community" style={navLinkStyle}>커뮤니티</Link>
        </div>

        {/* Auth Buttons */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          {user ? (
            <>
              <span style={{
                color: 'rgba(255, 255, 255, 0.8)',
                fontSize: '0.9rem'
              }}>
                {user.username}님
              </span>
              <Link to="/my-recipes" style={{
                color: '#D4A574',
                textDecoration: 'none',
                fontSize: '0.9rem',
                fontWeight: '500'
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
                  transition: 'all 0.3s ease'
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
                fontWeight: '500'
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
                transition: 'all 0.3s ease'
              }}>
                회원가입
              </Link>
            </>
          )}
        </div>
      </div>
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

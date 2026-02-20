import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    if (isMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
  }, [isMenuOpen]);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMenuOpen(false);
  };

  const categories = [
    { name: '☕ Beans', link: '/beans' },
    { name: '📃 Recipes', link: '/recipes' },
    { name: '📰 Articles', link: '/articles' },
    { name: '🦾 Gears', link: '/gears' },
    { name: '💬 Community', link: '/community' },
  ];

  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      background: 'rgba(26, 26, 26, 0.95)',
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '1rem 2rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        height: '70px'
      }}>
        <Link to="/" onClick={() => setIsMenuOpen(false)} style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '12px', 
          textDecoration: 'none',
          zIndex: 1100 
        }}>
          <img 
            src="/bean-logo.png" 
            alt="BeanDebug Logo" 
            style={{ 
              height: '32px', 
              width: 'auto',
            }} 
          />
          <span style={{ 
            fontFamily: "'Lora', serif", 
            fontSize: '1.5rem', 
            fontWeight: '700', 
            color: '#ffffff',
            letterSpacing: '-0.5px'
          }}>
            Bean Debug
          </span>
        </Link>

        <div className="nav-menu" style={{ display: 'flex', alignItems: 'center', gap: '2rem', flex: 1, justifyContent: 'center' }}>
          {categories.map((cat, index) => (
            <Link key={index} to={cat.link} className="nav-link-desktop">
              {cat.name}
            </Link>
          ))}
        </div>

        <div className="auth-buttons" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {user ? (
            <>
              <span className="user-tag">@{user.username}</span>
              <button onClick={handleLogout} className="logout-btn">logout()</button>
            </>
          ) : (
            <>
              <Link to="/login" className="login-btn">login()</Link>
              <Link to="/register" className="register-btn-desktop">register()</Link>
            </>
          )}
        </div>

        <button
          className="mobile-menu-btn"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          style={{
            zIndex: 1100,
            background: 'transparent',
            border: 'none',
            color: isMenuOpen ? '#00ff88' : '#fff',
            fontSize: '1.8rem',
            cursor: 'pointer',
            transition: 'all 0.3s ease'
          }}
        >
          {isMenuOpen ? '✕' : '☰'}
        </button>
      </div>

      <div className={`mobile-overlay ${isMenuOpen ? 'open' : ''}`}>
        <div className="mobile-menu-content">
          {categories.map((cat, index) => {
            const [emoji, ...nameParts] = cat.name.split(' ');
            const name = nameParts.join(' ');
            
            return (
              <Link
                key={index}
                to={cat.link}
                onClick={() => setIsMenuOpen(false)}
                className="mobile-nav-link"
                style={{ transitionDelay: `${index * 0.1}s` }}
              >
                <span className="mobile-emoji">{emoji}</span>
                <div className="mobile-text-wrapper">
                  <span className="mobile-cat-name">{name}</span>
                  <span className="mobile-cat-sub">fetch_{name.toLowerCase()}()</span>
                </div>
              </Link>
            );
          })}
          
          <div className="mobile-auth-section" style={{ transitionDelay: '0.6s' }}>
            {user ? (
              <button onClick={handleLogout} className="mobile-logout-btn">
                exit_session()
              </button>
            ) : (
              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', width: '100%' }}>
                <Link to="/login" onClick={() => setIsMenuOpen(false)} className="mobile-login-btn">login()</Link>
                <Link to="/register" onClick={() => setIsMenuOpen(false)} className="mobile-reg-btn">register()</Link>
              </div>
            )}
          </div>
        </div>
      </div>

      <style>{`
        .nav-link-desktop {
          color: rgba(255, 255, 255, 0.7);
          text-decoration: none;
          font-family: 'Fira Code', monospace;
          font-size: 0.9rem;
          transition: all 0.3s ease;
          border-bottom: 2px solid transparent;
          padding: 5px 0;
        }
        .nav-link-desktop:hover {
          color: #00ff88;
          border-bottom: 2px solid #00ff88;
        }
        .user-tag { color: #00ff88; font-family: 'Fira Code', monospace; font-size: 0.85rem; }
        .logout-btn {
          background: transparent; border: 1px solid #ff5555; color: #ff5555;
          padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer;
          font-family: 'Fira Code', monospace; transition: 0.3s;
        }
        .logout-btn:hover { background: #ff5555; color: #0a0a0a; }
        .login-btn {
          color: #8be9fd; border: 1px solid #8be9fd; padding: 0.5rem 1rem;
          border-radius: 6px; text-decoration: none; font-family: 'Fira Code', monospace;
          transition: 0.3s;
        }
        .login-btn:hover { background: rgba(139, 233, 253, 0.1); }
        .register-btn-desktop {
          background: #00ff88; color: #000; padding: 0.5rem 1rem;
          border-radius: 6px; text-decoration: none; font-family: 'Fira Code', monospace;
          font-weight: 700; font-size: 0.9rem; transition: 0.3s;
        }
        .register-btn-desktop:hover { background: #00cc6e; transform: translateY(-1px); }
        .mobile-overlay {
          position: fixed; top: 0; left: 0; width: 100%; height: 100vh;
          background: rgba(10, 10, 10, 0.98);
          display: flex; flex-direction: column; justify-content: center; align-items: center;
          opacity: 0; visibility: hidden; transform: translateY(-20px);
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          z-index: 1050;
        }
        .mobile-overlay.open { opacity: 1; visibility: visible; transform: translateY(0); }
        .mobile-menu-content { width: 100%; maxWidth: 320px; padding: 0 2rem; }
        .mobile-nav-link {
          display: flex; align-items: center; text-decoration: none;
          margin: 2rem 0; opacity: 0; transform: translateX(-20px);
          transition: all 0.4s ease;
        }
        .mobile-overlay.open .mobile-nav-link { opacity: 1; transform: translateX(0); }
        .mobile-emoji { font-size: 2.2rem; margin-right: 1.5rem; filter: drop-shadow(0 0 10px rgba(0, 255, 136, 0.4)); }
        .mobile-text-wrapper { display: flex; flex-direction: column; }
        .mobile-cat-name { color: #fff; font-size: 1.8rem; font-weight: 700; font-family: 'Fira Code', monospace; }
        .mobile-cat-sub { color: #00ff88; font-size: 0.75rem; font-family: 'Fira Code', monospace; opacity: 0.6; }
        .mobile-auth-section {
          margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1);
          display: flex; justify-content: center; opacity: 0; transition: 0.5s;
        }
        .mobile-overlay.open .mobile-auth-section { opacity: 1; }
        .mobile-login-btn, .mobile-reg-btn {
          flex: 1; padding: 0.8rem; text-align: center; border-radius: 8px;
          text-decoration: none; font-family: 'Fira Code', monospace; font-size: 0.9rem;
        }
        .mobile-login-btn { color: #8be9fd; border: 1px solid #8be9fd; }
        .mobile-reg-btn { background: #00ff88; color: #000; font-weight: 700; }
        .mobile-logout-btn {
          width: 100%; padding: 1rem; background: transparent; border: 1px solid #ff5555;
          color: #ff5555; border-radius: 8px; font-family: 'Fira Code', monospace;
        }

        @media (min-width: 769px) {
          .mobile-menu-btn, .mobile-overlay { display: none !important; }
          .nav-menu, .auth-buttons { display: flex !important; }
        }
        @media (max-width: 768px) {
          .nav-menu, .auth-buttons { display: none !important; }
          .mobile-menu-btn { display: block !important; }
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
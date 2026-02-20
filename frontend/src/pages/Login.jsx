import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(username, password);
      navigate('/');
    } catch (err) {
      setError('Authentication failed: Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
      padding: '2rem',
      paddingTop: '120px'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '480px'
      }}>
        {/* Terminal Window */}
        <div style={{
          background: '#1e1e1e',
          borderRadius: '12px',
          overflow: 'hidden',
          boxShadow: '0 25px 50px rgba(0, 0, 0, 0.5)',
          border: '1px solid #333'
        }}>
          {/* Terminal Header */}
          <div style={{
            background: '#2d2d2d',
            padding: '12px 16px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            borderBottom: '1px solid #333'
          }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ff5f56' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ffbd2e' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#27ca3f' }}></div>
            <span style={{
              marginLeft: '12px',
              color: '#888',
              fontFamily: "'Fira Code', monospace",
              fontSize: '0.85rem'
            }}>
              beandebug@login ~ 
            </span>
          </div>

          {/* Terminal Body */}
          <div style={{ padding: '2rem' }}>
            {/* Title */}
            <div style={{
              fontFamily: "'Fira Code', monospace",
              marginBottom: '1.5rem'
            }}>
              <div style={{ color: '#888', fontSize: '0.85rem' }}>
                {/* Welcome message */}
                <span style={{ color: '#00ff88' }}>$</span> ./authenticate.sh
              </div>
              <div style={{
                color: '#00ff88',
                fontSize: '1.5rem',
                fontWeight: '600',
                marginTop: '0.5rem'
              }}>
                Bean Debug Login
              </div>
              <div style={{ color: '#666', fontSize: '0.85rem', marginTop: '0.25rem' }}>
                // Enter your credentials to continue
              </div>
            </div>

            <form onSubmit={handleSubmit}>
              {error && (
                <div style={{
                  background: 'rgba(255, 0, 0, 0.1)',
                  border: '1px solid #ff4444',
                  borderRadius: '6px',
                  padding: '12px',
                  marginBottom: '1.5rem',
                  fontFamily: "'Fira Code', monospace",
                  fontSize: '0.85rem'
                }}>
                  <span style={{ color: '#ff4444' }}>✗ Error:</span>
                  <span style={{ color: '#ff6b6b', marginLeft: '8px' }}>{error}</span>
                </div>
              )}

              {/* Username Field */}
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{
                  display: 'block',
                  fontFamily: "'Fira Code', monospace",
                  fontSize: '0.85rem',
                  color: '#888',
                  marginBottom: '8px'
                }}>
                  <span style={{ color: '#ff79c6' }}>const</span>
                  <span style={{ color: '#f8f8f2' }}> username</span>
                  <span style={{ color: '#ff79c6' }}> =</span>
                </label>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder='"your_username"'
                  style={{
                    width: '100%',
                    padding: '14px 16px',
                    background: '#0a0a0a',
                    border: '1px solid #333',
                    borderRadius: '6px',
                    color: '#f8f8f2',
                    fontFamily: "'Fira Code', monospace",
                    fontSize: '0.95rem',
                    outline: 'none',
                    transition: 'border-color 0.3s ease',
                    boxSizing: 'border-box'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#00ff88'}
                  onBlur={(e) => e.target.style.borderColor = '#333'}
                />
              </div>

              {/* Password Field */}
              <div style={{ marginBottom: '2rem' }}>
                <label style={{
                  display: 'block',
                  fontFamily: "'Fira Code', monospace",
                  fontSize: '0.85rem',
                  color: '#888',
                  marginBottom: '8px'
                }}>
                  <span style={{ color: '#ff79c6' }}>const</span>
                  <span style={{ color: '#f8f8f2' }}> password</span>
                  <span style={{ color: '#ff79c6' }}> =</span>
                </label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder='"••••••••"'
                  style={{
                    width: '100%',
                    padding: '14px 16px',
                    background: '#0a0a0a',
                    border: '1px solid #333',
                    borderRadius: '6px',
                    color: '#f8f8f2',
                    fontFamily: "'Fira Code', monospace",
                    fontSize: '0.95rem',
                    outline: 'none',
                    transition: 'border-color 0.3s ease',
                    boxSizing: 'border-box'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#00ff88'}
                  onBlur={(e) => e.target.style.borderColor = '#333'}
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                style={{
                  width: '100%',
                  padding: '14px',
                  background: loading ? '#1a4d2e' : '#00ff88',
                  border: 'none',
                  borderRadius: '6px',
                  color: '#0a0a0a',
                  fontFamily: "'Fira Code', monospace",
                  fontSize: '1rem',
                  fontWeight: '600',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  transition: 'all 0.3s ease',
                  opacity: loading ? 0.7 : 1
                }}
                onMouseOver={(e) => !loading && (e.target.style.boxShadow = '0 0 20px rgba(0, 255, 136, 0.4)')}
                onMouseOut={(e) => e.target.style.boxShadow = 'none'}
              >
                {loading ? '> Authenticating...' : '> login()'}
              </button>
            </form>

            {/* Register Link */}
            <div style={{
              marginTop: '2rem',
              textAlign: 'center',
              fontFamily: "'Fira Code', monospace",
              fontSize: '0.85rem'
            }}>
              <span style={{ color: '#666' }}>// New user? </span>
              <Link
                to="/register"
                style={{
                  color: '#00ff88',
                  textDecoration: 'none',
                  transition: 'color 0.3s ease'
                }}
                onMouseOver={(e) => e.target.style.color = '#66ffaa'}
                onMouseOut={(e) => e.target.style.color = '#00ff88'}
              >
                register()
              </Link>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div style={{
          textAlign: 'center',
          marginTop: '1.5rem',
          fontFamily: "'Fira Code', monospace",
          fontSize: '0.75rem',
          color: '#444'
        }}>
          <span style={{ color: '#00ff88' }}>●</span> Secure connection established
        </div>
      </div>
    </div>
  );
};

export default Login;
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <span className="text-2xl font-bold text-coffee-700">
                ☕ Bean Debug
              </span>
            </Link>
            <div className="hidden md:flex ml-10 space-x-8">
              <Link to="/beans" className="text-gray-700 hover:text-coffee-600">
                Bean
              </Link>
              <Link to="/recipes" className="text-gray-700 hover:text-coffee-600">
                Recipes
              </Link>
              <Link to="/articles" className="text-gray-700 hover:text-coffee-600">
                Article
              </Link>
              <Link to="/gears" className="text-gray-700 hover:text-coffee-600">
                Gear Recommend
              </Link>
              <Link to="/community" className="text-gray-700 hover:text-coffee-600">
                Community
              </Link>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <span className="text-gray-700">
                  Welcome, {user.username}
                </span>
                <Link to="/my-beans" className="btn-secondary">
                  My Beans
                </Link>
                <Link to="/my-recipes" className="btn-secondary">
                  My Recipes
                </Link>
                <button onClick={handleLogout} className="btn-primary">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn-secondary">
                  Login
                </Link>
                <Link to="/register" className="btn-primary">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
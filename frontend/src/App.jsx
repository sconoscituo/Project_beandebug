import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Recipes from './pages/Recipes';
import Beans from './pages/Beans';
import Articles from './pages/Articles';
import RecipeDetail from './pages/RecipeDetail';


function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/recipes" element={<Recipes />} />
            <Route path="/beans" element={<Beans />} />
            <Route path="/articles" element={<Articles />} />
            <Route path="/recipes/:id" element={<RecipeDetail />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
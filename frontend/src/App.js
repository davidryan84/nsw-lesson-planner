import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import './styles/index.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  return (
    <BrowserRouter>
      <div className="app">
        {isAuthenticated && (
          <nav className="navbar" style={{ backgroundColor: '#2D8B3D' }}>
            <div className="nav-container">
              <Link to="/" className="nav-logo">NSW Lesson Planner</Link>
              <button onClick={() => {
                setIsAuthenticated(false);
                setCurrentUser(null);
              }}>Logout</button>
            </div>
          </nav>
        )}
        
        <Routes>
          <Route 
            path="/" 
            element={isAuthenticated ? <DashboardPage user={currentUser} /> : <LoginPage setAuth={setIsAuthenticated} setUser={setCurrentUser} />}
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;

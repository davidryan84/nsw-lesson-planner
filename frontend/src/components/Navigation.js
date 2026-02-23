import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Navigation.css';

function Navigation({ onLogout }) {
  const location = useLocation();

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>📚 NSW Planner</h2>
      </div>

      <nav className="nav-links">
        <li><Link to="/" className={isActive('/')}>Dashboard</Link></li>
        <li><Link to="/learning-experiences" className={isActive('/learning-experiences')}>Learning Experiences</Link></li>
        <li><Link to="/planner" className={isActive('/planner')}>Weekly Planner</Link></li>
        <li><Link to="/worksheets/new" className={isActive('/worksheets')}>Worksheets</Link></li>
        <li><Link to="/evidence" className={isActive('/evidence')}>Evidence Tracker</Link></li>
        <li><Link to="/progress" className={isActive('/progress')}>Progress</Link></li>
        <li><Link to="/pacing" className={isActive('/pacing')}>Pacing</Link></li>
      </nav>

      <div className="sidebar-footer">
        <button className="btn btn-secondary" onClick={onLogout}>
          Logout
        </button>
      </div>
    </div>
  );
}

export default Navigation;

import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { lessonApi } from '../api/lessonApi';
import { evidenceApi } from '../api/evidenceApi';
import Navigation from '../components/Navigation';
import '../styles/Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);
  const [lessons, setLessons] = useState([]);
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalLessons: 0,
    publishedLessons: 0,
    taughtLessons: 0,
    students: 0
  });

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const lessonsRes = await lessonApi.getAll();
      const lessons = lessonsRes.data.lessons || [];
      setLessons(lessons.slice(0, 5)); // Show 5 most recent

      // Calculate stats
      const published = lessons.filter(l => l.status === 'published').length;
      const taught = lessons.filter(l => l.status === 'taught').length;

      setStats({
        totalLessons: lessons.length,
        publishedLessons: published,
        taughtLessons: taught,
        students: 0 // Would come from student API
      });

      setLoading(false);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="app-container">
      <Navigation onLogout={handleLogout} />
      
      <div className="main-content">
        <div className="header">
          <h1>Dashboard</h1>
          <p>Welcome back! Here's your teaching overview.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-3">
          <div className="stat-card">
            <div className="stat-number">{stats.totalLessons}</div>
            <div className="stat-label">Total Lessons</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.publishedLessons}</div>
            <div className="stat-label">Published</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.taughtLessons}</div>
            <div className="stat-label">Taught</div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h2>Quick Actions</h2>
          <div className="quick-actions">
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/learning-experiences')}
            >
              Create Learning Experience
            </button>
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/planner')}
            >
              Plan This Week
            </button>
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/evidence')}
            >
              Log Student Evidence
            </button>
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/progress')}
            >
              View Progress
            </button>
          </div>
        </div>

        {/* Recent Lessons */}
        <div className="card">
          <h2>Recent Lessons</h2>
          {lessons.length > 0 ? (
            <table className="table">
              <thead>
                <tr>
                  <th>Unit</th>
                  <th>Learning Experience</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {lessons.map(lesson => (
                  <tr key={lesson.id}>
                    <td>Unit {lesson.learning_experience_id}</td>
                    <td>LE Lesson</td>
                    <td>
                      <span className={`badge badge-${lesson.status === 'published' ? 'info' : lesson.status === 'taught' ? 'success' : 'warning'}`}>
                        {lesson.status}
                      </span>
                    </td>
                    <td>{new Date(lesson.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No lessons yet. <a href="/learning-experiences">Create one now!</a></p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

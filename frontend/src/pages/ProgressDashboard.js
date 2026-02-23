import React, { useState, useEffect } from 'react';
import { evidenceApi } from '../api/evidenceApi';
import Navigation from '../components/Navigation';
import '../styles/ProgressDashboard.css';

function ProgressDashboard() {
  const [studentId, setStudentId] = useState('');
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadProgress = async (id) => {
    if (!id) return;
    
    setLoading(true);
    try {
      const res = await evidenceApi.getProgress(id);
      setProgress(res.data.progress || []);
    } catch (error) {
      console.error('Failed to load progress:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMasteryLevel = (level) => {
    const levels = {
      1: { label: 'Developing', color: '#F44336' },
      2: { label: 'Approaching', color: '#FF9800' },
      3: { label: 'Meeting', color: '#2196F3' },
      4: { label: 'Exceeding', color: '#4CAF50' }
    };
    return levels[level] || { label: 'Unknown', color: '#999' };
  };

  const getTrendIcon = (trend) => {
    const icons = {
      'improving': '📈',
      'stable': '➡️',
      'declining': '📉'
    };
    return icons[trend] || '❓';
  };

  return (
    <div className="app-container">
      <Navigation />
      
      <div className="main-content">
        <div className="header">
          <h1>Progress Dashboard</h1>
          <p>Track student mastery and learning progress</p>
        </div>

        <div className="card">
          <h2>Student Search</h2>
          <div className="form-group">
            <label>Enter Student ID or Name</label>
            <input
              type="text"
              value={studentId}
              onChange={(e) => {
                setStudentId(e.target.value);
                loadProgress(e.target.value);
              }}
              placeholder="Search for a student..."
            />
          </div>
        </div>

        {loading && <div className="loading">Loading...</div>}

        {!loading && progress.length > 0 && (
          <div className="progress-list">
            {progress.map(p => {
              const masteryInfo = getMasteryLevel(p.mastery_level);
              const scStatus = p.success_criteria_status || {};
              const metCount = Object.values(scStatus).filter(s => s === 'met').length;
              const totalCount = Object.keys(scStatus).length;

              return (
                <div key={p.id} className="progress-card">
                  <div className="progress-header">
                    <h3>Learning Experience {p.learning_experience_id}</h3>
                    <span 
                      className="badge"
                      style={{backgroundColor: masteryInfo.color}}
                    >
                      {masteryInfo.label}
                    </span>
                  </div>

                  <div className="progress-metrics">
                    <div className="metric">
                      <label>Mastery Level</label>
                      <div className="progress-bar">
                        <div 
                          className="progress-fill"
                          style={{
                            width: `${(p.mastery_level / 4) * 100}%`,
                            backgroundColor: masteryInfo.color
                          }}
                        />
                      </div>
                      <p>{p.mastery_level}/4</p>
                    </div>

                    <div className="metric">
                      <label>Success Criteria Met</label>
                      <p className="sc-count">{metCount} of {totalCount}</p>
                    </div>

                    <div className="metric">
                      <label>Trend</label>
                      <p className="trend">{getTrendIcon(p.trend)} {p.trend}</p>
                    </div>

                    <div className="metric">
                      <label>Evidence Collected</label>
                      <p>{p.evidence_count} observations</p>
                    </div>
                  </div>

                  {totalCount > 0 && (
                    <div className="success-criteria">
                      <h4>Success Criteria</h4>
                      <div className="criteria-list">
                        {Object.entries(scStatus).map(([id, status]) => (
                          <div key={id} className={`criterion criterion-${status}`}>
                            <span className="icon">{status === 'met' ? '✓' : '◐'}</span>
                            <span>Success Criterion {parseInt(id) + 1}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {!loading && studentId && progress.length === 0 && (
          <div className="card">
            <p>No progress data found for this student yet.</p>
          </div>
        )}

        {!studentId && !loading && (
          <div className="card">
            <p>Enter a student ID to view their progress.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProgressDashboard;

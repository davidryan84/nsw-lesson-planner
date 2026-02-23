import React, { useState, useEffect } from 'react';
import { learningExperienceApi } from '../api/learningExperienceApi';
import { lessonApi } from '../api/lessonApi';
import Navigation from '../components/Navigation';
import '../styles/ClassPacing.css';

function ClassPacing() {
  const [les, setLes] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [lesRes, lessonsRes] = await Promise.all([
        learningExperienceApi.getAll(),
        lessonApi.getAll()
      ]);
      
      setLes(lesRes.data.learning_experiences || []);
      setLessons(lessonsRes.data.lessons || []);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  // Group LEs by unit
  const lesByUnit = {};
  les.forEach(le => {
    if (!lesByUnit[le.unit_number]) {
      lesByUnit[le.unit_number] = [];
    }
    lesByUnit[le.unit_number].push(le);
  });

  return (
    <div className="app-container">
      <Navigation />
      
      <div className="main-content">
        <div className="header">
          <h1>Class Pacing Guide</h1>
          <p>Monitor progress through units and learning experiences</p>
        </div>

        <div className="pacing-overview">
          {Object.keys(lesByUnit).sort().map(unitNum => {
            const unitLes = lesByUnit[unitNum];
            const unitLessons = lessons.filter(l => 
              unitLes.some(le => le.id === l.learning_experience_id)
            );
            const taughtCount = unitLessons.filter(l => l.status === 'taught').length;
            const publishedCount = unitLessons.filter(l => 
              l.status === 'published' || l.status === 'taught'
            ).length;

            return (
              <div key={unitNum} className="unit-card">
                <div className="unit-header">
                  <h3>Unit {unitNum}</h3>
                  <div className="unit-stats">
                    <span className="stat">
                      <span className="number">{taughtCount}</span>
                      <span className="label">Taught</span>
                    </span>
                    <span className="stat">
                      <span className="number">{publishedCount}</span>
                      <span className="label">Planned</span>
                    </span>
                  </div>
                </div>

                <div className="les-list">
                  {unitLes.map(le => {
                    const leLessons = lessons.filter(l => l.learning_experience_id === le.id);
                    const status = leLessons.length === 0 ? 'not-started' 
                      : leLessons.some(l => l.status === 'taught') ? 'taught'
                      : leLessons.some(l => l.status === 'published') ? 'planned'
                      : 'draft';

                    return (
                      <div key={le.id} className={`le-entry le-${status}`}>
                        <div className="le-title">
                          <span className="status-indicator"></span>
                          <span>LE {le.experience_number}: {le.core_concept}</span>
                        </div>
                        <div className="le-info">
                          <span className={`badge badge-${status}`}>
                            {status === 'not-started' ? 'Not Started'
                              : status === 'draft' ? 'In Progress'
                              : status === 'planned' ? 'Planned'
                              : 'Taught'}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>

        <div className="card">
          <h2>Pacing Legend</h2>
          <div className="legend">
            <div className="legend-item">
              <span className="legend-color" style={{backgroundColor: '#F44336'}}></span>
              <span>Not Started</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{backgroundColor: '#FF9800'}}></span>
              <span>In Progress</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{backgroundColor: '#2196F3'}}></span>
              <span>Planned</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{backgroundColor: '#4CAF50'}}></span>
              <span>Taught</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ClassPacing;

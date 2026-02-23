import React, { useState, useEffect } from 'react';
import { learningExperienceApi } from '../api/learningExperienceApi';
import Navigation from '../components/Navigation';
import '../styles/LearningExperiences.css';

function LearningExperiences() {
  const [les, setLes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    unit_number: '',
    experience_number: '',
    core_concept: '',
    learning_intention: '',
    success_criteria: '',
    subject: 'Maths',
    year_level: 6
  });

  useEffect(() => {
    loadLEs();
  }, []);

  const loadLEs = async () => {
    try {
      const res = await learningExperienceApi.getAll();
      setLes(res.data.learning_experiences || []);
    } catch (error) {
      console.error('Failed to load learning experiences:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const scArray = formData.success_criteria
        .split('\n')
        .map(sc => sc.trim())
        .filter(sc => sc);

      await learningExperienceApi.create({
        ...formData,
        success_criteria: scArray
      });

      setShowForm(false);
      setFormData({
        unit_number: '',
        experience_number: '',
        core_concept: '',
        learning_intention: '',
        success_criteria: '',
        subject: 'Maths',
        year_level: 6
      });
      loadLEs();
    } catch (error) {
      console.error('Failed to create LE:', error);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="app-container">
      <Navigation />
      
      <div className="main-content">
        <div className="header">
          <h1>Learning Experiences</h1>
          <button 
            className="btn btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Cancel' : 'Create New LE'}
          </button>
        </div>

        {showForm && (
          <div className="card">
            <h2>Create Learning Experience</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-row">
                <div className="form-group">
                  <label>Unit Number</label>
                  <input
                    type="number"
                    value={formData.unit_number}
                    onChange={(e) => setFormData({...formData, unit_number: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Experience Number</label>
                  <input
                    type="number"
                    value={formData.experience_number}
                    onChange={(e) => setFormData({...formData, experience_number: e.target.value})}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Subject</label>
                <select
                  value={formData.subject}
                  onChange={(e) => setFormData({...formData, subject: e.target.value})}
                >
                  <option>Maths</option>
                  <option>English</option>
                  <option>Science</option>
                  <option>History</option>
                  <option>Geography</option>
                </select>
              </div>

              <div className="form-group">
                <label>Core Concept</label>
                <input
                  type="text"
                  value={formData.core_concept}
                  onChange={(e) => setFormData({...formData, core_concept: e.target.value})}
                  placeholder="e.g., Fractions, Photosynthesis"
                  required
                />
              </div>

              <div className="form-group">
                <label>Learning Intention</label>
                <textarea
                  value={formData.learning_intention}
                  onChange={(e) => setFormData({...formData, learning_intention: e.target.value})}
                  placeholder="What will students learn?"
                  required
                />
              </div>

              <div className="form-group">
                <label>Success Criteria (one per line)</label>
                <textarea
                  value={formData.success_criteria}
                  onChange={(e) => setFormData({...formData, success_criteria: e.target.value})}
                  placeholder="I can identify fractions&#10;I can compare fractions&#10;I can order fractions"
                  required
                />
              </div>

              <button type="submit" className="btn btn-primary">Create LE</button>
            </form>
          </div>
        )}

        <div className="grid grid-2">
          {les.map(le => (
            <div key={le.id} className="le-card">
              <div className="le-header">
                <h3>Unit {le.unit_number} - LE {le.experience_number}</h3>
                <span className="badge badge-info">{le.subject}</span>
              </div>
              
              <h4>{le.core_concept}</h4>
              
              <div className="le-section">
                <strong>Learning Intention:</strong>
                <p>{le.learning_intention}</p>
              </div>
              
              <div className="le-section">
                <strong>Success Criteria:</strong>
                <ul>
                  {Array.isArray(le.success_criteria) && le.success_criteria.map((sc, idx) => (
                    <li key={idx}>{sc}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default LearningExperiences;

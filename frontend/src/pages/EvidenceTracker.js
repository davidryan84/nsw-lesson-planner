import React, { useState, useEffect } from 'react';
import { evidenceApi } from '../api/evidenceApi';
import { learningExperienceApi } from '../api/learningExperienceApi';
import Navigation from '../components/Navigation';
import '../styles/EvidenceTracker.css';

function EvidenceTracker() {
  const [evidence, setEvidence] = useState([]);
  const [les, setLes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [formData, setFormData] = useState({
    student_id: '',
    learning_experience_id: '',
    observation_text: '',
    mastery_level: 3,
    success_criteria_ids: [],
    notes: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const lesRes = await learningExperienceApi.getAll();
      setLes(lesRes.data.learning_experiences || []);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      await evidenceApi.log({
        ...formData,
        observation_date: new Date().toISOString()
      });

      setShowForm(false);
      setFormData({
        student_id: '',
        learning_experience_id: '',
        observation_text: '',
        mastery_level: 3,
        success_criteria_ids: [],
        notes: ''
      });
      
      if (selectedStudent) {
        loadStudentEvidence(selectedStudent);
      }
    } catch (error) {
      console.error('Failed to log evidence:', error);
    }
  };

  const loadStudentEvidence = async (studentId) => {
    try {
      const res = await evidenceApi.getStudent(studentId);
      setEvidence(res.data.evidence || []);
    } catch (error) {
      console.error('Failed to load evidence:', error);
    }
  };

  const getMasteryLabel = (level) => {
    const labels = {
      1: 'Developing',
      2: 'Approaching',
      3: 'Meeting',
      4: 'Exceeding'
    };
    return labels[level] || 'Unknown';
  };

  const getMasteryColor = (level) => {
    const colors = {
      1: '#F44336',
      2: '#FF9800',
      3: '#2196F3',
      4: '#4CAF50'
    };
    return colors[level] || '#999';
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="app-container">
      <Navigation />
      
      <div className="main-content">
        <div className="header">
          <h1>Evidence Tracker</h1>
          <button 
            className="btn btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Cancel' : 'Log Evidence'}
          </button>
        </div>

        {showForm && (
          <div className="card">
            <h2>Log Student Evidence</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Student ID</label>
                <input
                  type="text"
                  value={formData.student_id}
                  onChange={(e) => setFormData({...formData, student_id: e.target.value})}
                  placeholder="Enter student name or ID"
                  required
                />
              </div>

              <div className="form-group">
                <label>Learning Experience</label>
                <select
                  value={formData.learning_experience_id}
                  onChange={(e) => setFormData({...formData, learning_experience_id: e.target.value})}
                  required
                >
                  <option value="">Select LE</option>
                  {les.map(le => (
                    <option key={le.id} value={le.id}>
                      Unit {le.unit_number} - LE {le.experience_number}: {le.core_concept}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Mastery Level</label>
                <div className="mastery-options">
                  {[1, 2, 3, 4].map(level => (
                    <label key={level} className="radio-option">
                      <input
                        type="radio"
                        name="mastery"
                        value={level}
                        checked={formData.mastery_level === level}
                        onChange={(e) => setFormData({...formData, mastery_level: parseInt(e.target.value)})}
                      />
                      <span style={{color: getMasteryColor(level)}}>
                        {level}. {getMasteryLabel(level)}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="form-group">
                <label>Observation</label>
                <textarea
                  value={formData.observation_text}
                  onChange={(e) => setFormData({...formData, observation_text: e.target.value})}
                  placeholder="What did you observe?"
                  required
                />
              </div>

              <div className="form-group">
                <label>Notes</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  placeholder="Any additional notes"
                />
              </div>

              <button type="submit" className="btn btn-primary">Log Evidence</button>
            </form>
          </div>
        )}

        <div className="card">
          <h2>Search Student Evidence</h2>
          <div className="form-group">
            <input
              type="text"
              placeholder="Enter student name or ID"
              onChange={(e) => {
                setSelectedStudent(e.target.value);
                if (e.target.value) {
                  loadStudentEvidence(e.target.value);
                } else {
                  setEvidence([]);
                }
              }}
            />
          </div>

          {evidence.length > 0 && (
            <div className="evidence-list">
              {evidence.map(e => (
                <div key={e.id} className="evidence-item">
                  <div className="evidence-header">
                    <h4>{e.learning_experience_id}</h4>
                    <span 
                      className="badge"
                      style={{backgroundColor: getMasteryColor(e.mastery_level)}}
                    >
                      {getMasteryLabel(e.mastery_level)}
                    </span>
                  </div>
                  
                  <p className="observation">{e.observation_text}</p>
                  
                  {e.notes && <p className="notes"><strong>Notes:</strong> {e.notes}</p>}
                  
                  <p className="date">
                    {new Date(e.observation_date).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}

          {selectedStudent && evidence.length === 0 && (
            <p>No evidence logged yet for this student.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default EvidenceTracker;

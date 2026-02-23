import React, { useState, useEffect } from 'react';
import { lessonApi } from '../api/lessonApi';
import { learningExperienceApi } from '../api/learningExperienceApi';
import { supportFilesApi } from '../api/supportFilesApi';
import Navigation from '../components/Navigation';
import '../styles/WeeklyPlanner.css';

function WeeklyPlanner() {
  const [week, setWeek] = useState(1);
  const [lessons, setLessons] = useState([]);
  const [les, setLes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    learning_experience_id: '',
    week_number: 1,
    date_scheduled: new Date().toISOString().split('T')[0],
    duration_minutes: 60,
    location: '',
    notes: ''
  });

  useEffect(() => {
    loadData();
  }, [week]);

  const loadData = async () => {
    try {
      const lessonsRes = await lessonApi.getWeek(week);
      const lesRes = await learningExperienceApi.getAll();
      
      setLessons(lessonsRes.data.lessons || []);
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
      await lessonApi.create({
        ...formData,
        week_number: week,
        status: 'draft'
      });

      setShowForm(false);
      setFormData({
        learning_experience_id: '',
        week_number: week,
        date_scheduled: new Date().toISOString().split('T')[0],
        duration_minutes: 60,
        location: '',
        notes: ''
      });
      loadData();
    } catch (error) {
      console.error('Failed to create lesson:', error);
    }
  };

  const handlePublish = async (lessonId) => {
    try {
      await lessonApi.publish(lessonId);
      loadData();
    } catch (error) {
      console.error('Failed to publish:', error);
    }
  };

  const handleGenerateFiles = async (lessonId) => {
    try {
      await supportFilesApi.generateAll(lessonId);
      alert('Support files generated successfully!');
    } catch (error) {
      console.error('Failed to generate files:', error);
    }
  };

  if (loading) return <div>Loading...</div>;

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

  return (
    <div className="app-container">
      <Navigation />
      
      <div className="main-content">
        <div className="header">
          <h1>Weekly Planner - Week {week}</h1>
          <div className="week-nav">
            <button onClick={() => setWeek(Math.max(1, week - 1))} className="btn btn-secondary">
              ← Previous
            </button>
            <button onClick={() => setWeek(week + 1)} className="btn btn-secondary">
              Next →
            </button>
            <button 
              className="btn btn-primary"
              onClick={() => setShowForm(!showForm)}
            >
              {showForm ? 'Cancel' : 'Add Lesson'}
            </button>
          </div>
        </div>

        {showForm && (
          <div className="card">
            <h2>Add Lesson to Week {week}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Learning Experience</label>
                <select
                  value={formData.learning_experience_id}
                  onChange={(e) => setFormData({...formData, learning_experience_id: e.target.value})}
                  required
                >
                  <option value="">Select a Learning Experience</option>
                  {les.map(le => (
                    <option key={le.id} value={le.id}>
                      Unit {le.unit_number} - LE {le.experience_number}: {le.core_concept}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Date</label>
                  <input
                    type="date"
                    value={formData.date_scheduled}
                    onChange={(e) => setFormData({...formData, date_scheduled: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Duration (minutes)</label>
                  <input
                    type="number"
                    value={formData.duration_minutes}
                    onChange={(e) => setFormData({...formData, duration_minutes: parseInt(e.target.value)})}
                    min="15"
                    max="180"
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Location</label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({...formData, location: e.target.value})}
                  placeholder="e.g., Classroom A, Gym"
                />
              </div>

              <div className="form-group">
                <label>Notes</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  placeholder="Any special notes or materials needed?"
                />
              </div>

              <button type="submit" className="btn btn-primary">Add Lesson</button>
            </form>
          </div>
        )}

        <div className="planner-grid">
          {days.map(day => (
            <div key={day} className="planner-day">
              <h3>{day}</h3>
              <div className="lessons-list">
                {lessons.filter(l => {
                  const lessonDate = new Date(l.date_scheduled);
                  const dayIndex = days.indexOf(day);
                  const weekStart = new Date();
                  weekStart.setDate(weekStart.getDate() - weekStart.getDay() + 1 + (dayIndex));
                  
                  return lessonDate.toDateString() === weekStart.toDateString();
                }).map(lesson => (
                  <div key={lesson.id} className={`lesson-item lesson-${lesson.status}`}>
                    <h4>LE {lesson.learning_experience_id}</h4>
                    <p className="duration">{lesson.duration_minutes} min</p>
                    {lesson.location && <p className="location">📍 {lesson.location}</p>}
                    
                    <div className="lesson-actions">
                      {lesson.status === 'draft' && (
                        <button 
                          className="btn btn-small btn-primary"
                          onClick={() => handlePublish(lesson.id)}
                        >
                          Publish
                        </button>
                      )}
                      <button 
                        className="btn btn-small btn-secondary"
                        onClick={() => handleGenerateFiles(lesson.id)}
                      >
                        Files
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {lessons.length === 0 && (
          <div className="card">
            <p>No lessons scheduled for week {week}. <a href="#" onClick={() => setShowForm(true)}>Add one now!</a></p>
          </div>
        )}
      </div>
    </div>
  );
}

export default WeeklyPlanner;

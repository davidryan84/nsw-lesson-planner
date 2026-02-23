import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { worksheetApi } from '../api/worksheetApi';
import Navigation from '../components/Navigation';
import '../styles/WorksheetGenerator.css';

function WorksheetGenerator() {
  const { lessonId } = useParams();
  const [worksheets, setWorksheets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [selectedTier, setSelectedTier] = useState(null);

  useEffect(() => {
    if (lessonId) {
      loadWorksheets();
    }
  }, [lessonId]);

  const loadWorksheets = async () => {
    try {
      const res = await worksheetApi.getLesson(lessonId);
      setWorksheets(res.data.worksheets || []);
    } catch (error) {
      console.error('Failed to load worksheets:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      await worksheetApi.generate(lessonId);
      loadWorksheets();
    } catch (error) {
      console.error('Failed to generate worksheets:', error);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  const tiers = [
    { name: 'Mild', color: '#FF9800', questions: 5 },
    { name: 'Medium', color: '#2196F3', questions: 10 },
    { name: 'Spicy', color: '#F44336', questions: 15 },
    { name: 'Enrichment', color: '#4CAF50', questions: 2 }
  ];

  return (
    <div className="app-container">
      <Navigation />
      
      <div className="main-content">
        <div className="header">
          <h1>Worksheet Generator</h1>
          <p>Generate and manage differentiated worksheets</p>
        </div>

        {worksheets.length === 0 ? (
          <div className="card">
            <h2>Generate Worksheets</h2>
            <p>No worksheets created yet for this lesson.</p>
            <button 
              className="btn btn-primary"
              onClick={handleGenerate}
              disabled={generating}
            >
              {generating ? 'Generating...' : 'Generate All Worksheets'}
            </button>
          </div>
        ) : (
          <>
            <div className="tiers-grid">
              {tiers.map(tier => {
                const ws = worksheets.find(w => w.tier === tier.name.toLowerCase());
                return (
                  <div key={tier.name} className="tier-card" style={{borderTopColor: tier.color}}>
                    <h3 style={{color: tier.color}}>{tier.name}</h3>
                    <div className="tier-info">
                      <p className="question-count">{tier.questions} Questions</p>
                      {ws && <span className="badge badge-success">Generated</span>}
                    </div>
                    <button 
                      className="btn btn-primary"
                      onClick={() => setSelectedTier(tier.name.toLowerCase())}
                    >
                      View Details
                    </button>
                  </div>
                );
              })}
            </div>

            {selectedTier && (
              <div className="card">
                <h2>{selectedTier.charAt(0).toUpperCase() + selectedTier.slice(1)} Tier Questions</h2>
                <div className="questions-list">
                  {worksheets.find(w => w.tier === selectedTier)?.questions?.map(q => (
                    <div key={q.id} className="question-item">
                      <h4>Q{q.question_number}: {q.question_text}</h4>
                      {q.hints && (
                        <div className="hints">
                          <strong>💡 Hint:</strong> {JSON.parse(q.hints)?.[0] || 'No hint'}
                        </div>
                      )}
                      {q.model_answer && (
                        <div className="answer">
                          <strong>Model Answer:</strong> {q.model_answer}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default WorksheetGenerator;

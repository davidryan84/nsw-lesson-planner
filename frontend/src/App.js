import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthContext, AuthProvider } from './context/AuthContext';
import './App.css';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import LearningExperiences from './pages/LearningExperiences';
import WeeklyPlanner from './pages/WeeklyPlanner';
import WorksheetGenerator from './pages/WorksheetGenerator';
import EvidenceTracker from './pages/EvidenceTracker';
import ProgressDashboard from './pages/ProgressDashboard';
import ClassPacing from './pages/ClassPacing';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useContext(AuthContext);
  
  if (loading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/login" />;
  
  return children;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* Protected routes */}
          <Route 
            path="/" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/learning-experiences" 
            element={
              <ProtectedRoute>
                <LearningExperiences />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/planner" 
            element={
              <ProtectedRoute>
                <WeeklyPlanner />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/worksheets/:lessonId" 
            element={
              <ProtectedRoute>
                <WorksheetGenerator />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/evidence" 
            element={
              <ProtectedRoute>
                <EvidenceTracker />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/progress" 
            element={
              <ProtectedRoute>
                <ProgressDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/pacing" 
            element={
              <ProtectedRoute>
                <ClassPacing />
              </ProtectedRoute>
            } 
          />
          
          {/* Catch all */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;

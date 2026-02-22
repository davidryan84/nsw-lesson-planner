import React from 'react';

function DashboardPage({ user }) {
  return (
    <div className="dashboard-container">
      <h1>Welcome, {user?.first_name}!</h1>
      <p>NSW Lesson Planner Dashboard</p>
      <div className="cards">
        <div className="card" style={{ borderLeft: `4px solid #2D8B3D` }}>
          <h3>Worksheets</h3>
          <p>Create and manage worksheets</p>
        </div>
        <div className="card" style={{ borderLeft: `4px solid #2D8B3D` }}>
          <h3>Students</h3>
          <p>Manage your students</p>
        </div>
        <div className="card" style={{ borderLeft: `4px solid #2D8B3D` }}>
          <h3>Evidence</h3>
          <p>Log student observations</p>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;

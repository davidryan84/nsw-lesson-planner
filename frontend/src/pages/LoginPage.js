import React, { useState } from 'react';
import axios from 'axios';

function LoginPage({ setAuth, setUser }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/v1/auth/login', {
        email,
        password
      });
      
      setAuth(true);
      setUser(response.data.teacher);
      localStorage.setItem('access_token', response.data.access_token);
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box" style={{ border: `2px solid #2D8B3D` }}>
        <h1 style={{ color: '#2D8B3D' }}>NSW Lesson Planner</h1>
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" style={{ backgroundColor: '#2D8B3D', color: 'white' }}>
            Login
          </button>
        </form>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    </div>
  );
}

export default LoginPage;

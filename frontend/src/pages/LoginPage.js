import React, { useState } from 'react';
import axios from 'axios';

function LoginPage({ setAuth, setUser }) {
  const [isRegistering, setIsRegistering] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
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

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      const response = await axios.post('http://localhost:5000/api/v1/auth/register', {
        email,
        password,
        first_name: firstName,
        last_name: lastName
      });
      
      setSuccess('Registration successful! Logging you in...');
      setAuth(true);
      setUser(response.data.teacher);
      localStorage.setItem('access_token', response.data.access_token);
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box" style={{ border: `2px solid #2D8B3D` }}>
        <h1 style={{ color: '#2D8B3D' }}>NSW Lesson Planner</h1>
        
        {isRegistering ? (
          <form onSubmit={handleRegister}>
            <h3 style={{ color: '#2D8B3D', marginBottom: '1rem' }}>Create Account</h3>
            <input
              type="text"
              placeholder="First Name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Last Name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
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
              Register
            </button>
            <p style={{ textAlign: 'center', marginTop: '1rem' }}>
              Already have an account? 
              <button 
                type="button"
                onClick={() => setIsRegistering(false)}
                style={{ background: 'none', border: 'none', color: '#2D8B3D', cursor: 'pointer', textDecoration: 'underline' }}
              >
                Login
              </button>
            </p>
          </form>
        ) : (
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
            <p style={{ textAlign: 'center', marginTop: '1rem' }}>
              Don't have an account? 
              <button 
                type="button"
                onClick={() => setIsRegistering(true)}
                style={{ background: 'none', border: 'none', color: '#2D8B3D', cursor: 'pointer', textDecoration: 'underline' }}
              >
                Register
              </button>
            </p>
          </form>
        )}
        
        {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}
        {success && <p style={{ color: 'green', marginTop: '1rem' }}>{success}</p>}
      </div>
    </div>
  );
}

export default LoginPage;

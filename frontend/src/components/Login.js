import React, { useState, useCallback } from 'react';
import  { useNavigate } from 'react-router-dom';
import api from '../services/api';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [timeoutId, setTimeoutId] = useState(null);
    const navigate = useNavigate();

    const validateForm = () => {
        if (!email || !password) {
            setError('Please fill in all fields');
            return false;
        }
        if (!/\S+@\S+\.\S+/.test(email)) {
            setError('Please enter a valid email address');
            return false;
        }
        return true;
    };

    const clearErrors = useCallback(() => {
        if (timeoutId) clearTimeout(timeoutId);
        setError('');
    }, [timeoutId]);

    const handleLogin = async (e) => {
        e.preventDefault();
        clearErrors();

        if (!validateForm()) return;

        setIsLoading(true);
        try {
            const response = await api.login({ email, password });
            // Ensure token is stored with Bearer prefix
            const token = response.data.token;
            localStorage.setItem('token', token.startsWith('Bearer ') ? token : `Bearer ${token}`);
            localStorage.setItem('user', JSON.stringify(response.data.user));
            navigate('/');
        } catch (error) {
            const errorMessage = error.message === 'Request timeout'
                ? 'Connection timeout. Please try again.'
                : error.response?.data?.message || 'Login failed. Please check your credentials.';
            setError(errorMessage);
            const id = setTimeout(() => setError(''), 5000);
            setTimeoutId(id);
        } finally {
            setIsLoading(false);
        }
    };

    const handleInputChange = (setter) => (e) => {
        setError('');
        setter(e.target.value);
    };

    return (
        <div className="auth-container">
            <form onSubmit={handleLogin} className="auth-form" autoComplete="on">
                {error && <div className="error-message" role="alert">{error}</div>}
                <h2>Login</h2>
                <input
                    type="email"
                    value={email}
                    onChange={handleInputChange(setEmail)}
                    placeholder="Email"
                    required
                    className="auth-input"
                    aria-label="Email address"
                    autoComplete="email"
                />
                <input
                    type="password"
                    value={password}
                    onChange={handleInputChange(setPassword)}
                    placeholder="Password"
                    required
                    className="auth-input"
                    aria-label="Password"
                    autoComplete="current-password"
                />
                <button
                    type="submit"
                    className="auth-button"
                    disabled={isLoading}
                >
                    {isLoading ? 'Logging in...' : 'Login'}
                </button>
                <p>Don't have an account? <span onClick={() => navigate('/register')} className="auth-link">Register</span></p>
            </form>
        </div>
    );
}

export default Login;

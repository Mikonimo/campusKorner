import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const Register = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        fullname: '',
        university: ''
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        setError('');
    };

    const validateForm = () => {
        if (!formData.email || !formData.password || !formData.fullname || !formData.university) {
            setError('All fields are required');
            return false;
        }
        if (!/\S+@\S+\.\S+/.test(formData.email)) {
            setError('Please enter a valid email address');
            return false;
        }
        return true;
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        if (!validateForm()) return;

        setIsLoading(true);
        try {
            const response = await api.register(formData);
            if (response.data.token) {
                // Ensure token is stored with Bearer prefix
                const token = response.data.token;
                localStorage.setItem('token', token.startsWith('Bearer ') ? token : `Bearer ${token}`);
                localStorage.setItem('user', JSON.stringify(response.data.user));
                navigate('/');  // Navigate to home instead of login since we have the token
            }
        } catch (error) {
            setError(error.response?.data?.message || 'Registration failed');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <form onSubmit={handleRegister} className="auth-form">
                <h2>Register</h2>
                {error && <div className="error-message" role="alert">{error}</div>}
                
                <input
                    type="text"
                    name="fullname"
                    value={formData.fullname}
                    onChange={handleChange}
                    placeholder="Full Name"
                    required
                    className="auth-input"
                    aria-label="Full name"
                />
                <input
                    type="text"
                    name="university"
                    value={formData.university}
                    onChange={handleChange}
                    placeholder="University"
                    required
                    className="auth-input"
                    aria-label="University"
                />
                <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Email"
                    required
                    className="auth-input"
                    aria-label="Email address"
                />
                <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Password"
                    required
                    className="auth-input"
                    aria-label="Password"
                />
                <button 
                    type="submit" 
                    className="auth-button"
                    disabled={isLoading}
                >
                    {isLoading ? 'Registering...' : 'Register'}
                </button>
                <p>Already have an account? <span onClick={() => navigate('/login')} className="auth-link">Login</span></p>
            </form>
        </div>
    );
};

export default Register;

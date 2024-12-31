import React from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const Navigation = () => {
    const isAuthenticated = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    const handleLogout = async () => {
        try {
            await api.logout();
        } catch (error) {
            console.error('Logout request failed:', error);
        } finally {
            localStorage.clear();
            window.location.href = '/login';
        }
    };

    return (
        <nav className="nav-container">
            <Link to="/" className="nav-brand">
                CampusKorner
            </Link>
            <div className="nav-links">
                {isAuthenticated ? (
                    <>
                        <Link to="/" className="nav-link">Products</Link>
                        <Link to="/cart" className="nav-link">Cart</Link>
                        <Link to="/profile" className="nav-link">
                            {user.fullname ? `Profile (${user.fullname})` : 'Profile'}
                        </Link>
                        <button onClick={handleLogout} className="nav-button">Logout</button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-link">Login</Link>
                        <Link to="/register" className="nav-link">Register</Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navigation;

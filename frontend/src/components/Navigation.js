import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
    const navigate = useNavigate();
    const isAuthenticated = !!localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const isSeller = user.is_seller;

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
    };

    return (
        <nav className="navigation">
            <div className="nav-brand" onClick={() => navigate('/')}>
                CampusKorner
            </div>
            <div className="nav-buttons">
                {isAuthenticated ? (
                    <>
                        <button onClick={() => navigate('/')}>Products</button>
                        {isSeller && (
                            <button onClick={() => navigate('/products')}>Sell</button>
                        )}
                        <button onClick={() => navigate('/cart')}>Cart</button>
                        <button onClick={() => navigate('/orders')}>Orders</button>
                        <button onClick={() => navigate('/profile')}>Profile</button>
                        <button onClick={handleLogout} className="logout">Logout</button>
                    </>
                ) : (
                    <>
                        <button onClick={() => navigate('/login')}>Login</button>
                        <button onClick={() => navigate('/register')}>Register</button>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navigation;

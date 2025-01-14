import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
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
            <Link to="/" className="nav-brand">
                CampusKorner
            </Link>
            <div className="nav-buttons">
                {isAuthenticated ? (
                    <>
                        <Link to="/" className="nav-link home">
                            Products
                        </Link>
                        {isSeller && (
                            <Link to="/products" className="nav-link sell">
                                Sell
                            </Link>
                        )}
                        <Link to="/cart" className="nav-link cart">
                            Cart
                            <div className="cart-badge">
                                {/* Add cart count if you have it */}
                                {/* <span className="cart-count">0</span> */}
                            </div>
                        </Link>
                        <Link to="/orders" className="nav-link orders">
                            Orders
                        </Link>
                        <Link to="/profile" className="nav-link profile">
                            Profile
                        </Link>
                        <button onClick={handleLogout} className="nav-button logout">
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-link login">
                            Login
                        </Link>
                        <Link to="/register" className="nav-link register">
                            Register
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navigation;

import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Cart = () => {
    const [cartItems, setCartItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [updateLoading, setUpdateLoading] = useState(false);

    useEffect(() => {
        fetchCart();
    }, []);

    const fetchCart = async () => {
        try {
            const response = await api.getCart();
            setCartItems(response.data.items || []);
        } catch (error) {
            setError('Failed to load cart items');
        } finally {
            setLoading(false);
        }
    };

    const updateQuantity = async (productId, newQuantity) => {
        if (newQuantity < 1) return;
        setUpdateLoading(true);
        try {
            await api.addToCart(productId, newQuantity);
            fetchCart();
        } catch (error) {
            setError('Failed to update quantity');
        } finally {
            setUpdateLoading(false);
        }
    };

    const removeItem = async (productId) => {
        try {
            await api.addToCart(productId, 0);
            fetchCart();
        } catch (error) {
            setError('Failed to remove item');
        }
    };

    const calculateTotal = () => {
        return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
    };

    const handleCheckout = async () => {
        try {
            await api.createOrder({ items: cartItems });
            setCartItems([]);
            alert('Order placed successfully!');
        } catch (error) {
            setError('Failed to place order');
        }
    };

    if (loading) return <div className="loading">Loading cart...</div>;
    if (error) return <div className="error-message">{error}</div>;

    return (
        <div className="cart-container">
            <h2>Your Cart</h2>
            {cartItems.length === 0 ? (
                <div className="empty-cart">
                    <p>Your cart is empty</p>
                </div>
            ) : (
                <>
                    <div className="cart-items">
                        {cartItems.map((item) => (
                            <div key={item.id} className="cart-item">
                                <div className="item-info">
                                    <h3>{item.name}</h3>
                                    <p className="item-price">
                                        ${item.price.toFixed(2)} x {item.quantity}
                                    </p>
                                </div>
                                <div className="item-actions">
                                    <button
                                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                        disabled={updateLoading || item.quantity <= 1}
                                        className="quantity-btn"
                                    >
                                        -
                                    </button>
                                    <span className="quantity">{item.quantity}</span>
                                    <button
                                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                        disabled={updateLoading}
                                        className="quantity-btn"
                                    >
                                        +
                                    </button>
                                    <button
                                        onClick={() => removeItem(item.id)}
                                        disabled={updateLoading}
                                        className="remove-btn"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="cart-summary">
                        <div className="cart-total">
                            <h3>Total: ${calculateTotal().toFixed(2)}</h3>
                        </div>
                        <button
                            onClick={handleCheckout}
                            disabled={updateLoading}
                            className="checkout-btn"
                        >
                            Proceed to Checkout
                        </button>
                    </div>
                </>
            )}
        </div>
    );
};

export default Cart;

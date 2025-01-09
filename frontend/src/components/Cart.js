import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const Cart = () => {
    const navigate = useNavigate();
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
            await api.updateCartItem(productId, newQuantity);
            await fetchCart();
        } catch (error) {
            setError('Failed to update quantity');
            console.error('Update quantity error:', error);
        } finally {
            setUpdateLoading(false);
        }
    };

    const removeItem = async (productId) => {
        setUpdateLoading(true);
        try {
            await api.removeFromCart(productId);
            await fetchCart();
        } catch (error) {
            setError('Failed to remove item');
            console.error('Remove item error:', error);
        } finally {
            setUpdateLoading(false);
        }
    };

    const clearCart = async () => {
        setUpdateLoading(true);
        try {
            await api.clearCart();
            setCartItems([]);
        } catch (error) {
            setError('Failed to clear cart');
            console.error('Clear cart error:', error);
        } finally {
            setUpdateLoading(false);
        }
    };

    const calculateTotal = () => {
        return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
    };

    const handleCheckout = async () => {
        try {
            if (cartItems.length === 0) {
                setError('Your cart is empty');
                return;
            }

            const orderItems = cartItems.map(item => ({
                id: item.product_id || item.id,
                quantity: item.quantity
            }));

            await api.createOrder(orderItems);
            await api.getCart();
            setCartItems([]);
            alert('Order placed successfully!');
            navigate('/orders');
        } catch (error) {
            console.error('Checkout error:', error);
            setError(error.response?.data?.error || 'Failed to place order');
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
                                        onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                                        disabled={updateLoading || item.quantity <= 1}
                                        className="quantity-btn"
                                    >
                                        -
                                    </button>
                                    <span className="quantity">{item.quantity}</span>
                                    <button
                                        onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                                        disabled={updateLoading}
                                        className="quantity-btn"
                                    >
                                        +
                                    </button>
                                    <button
                                        onClick={() => removeItem(item.product_id)}
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
                        <div className="cart-actions">
                            <button
                                onClick={clearCart}
                                disabled={updateLoading}
                                className="clear-cart-btn"
                            >
                                Clear Cart
                            </button>
                            <button
                                onClick={handleCheckout}
                                disabled={updateLoading}
                                className="checkout-btn"
                            >
                                Proceed to Checkout
                            </button>
                        </div>
                    </div>
                </>
            )}
            {error && <div className="error-message">{error}</div>}
        </div>
    );
};

export default Cart;

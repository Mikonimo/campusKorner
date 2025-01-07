import React, { useState, useEffect, useCallback } from 'react';
import api from '../services/api';
import './Orders.css';  // Add this import

const Orders = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [role, setRole] = useState('buyer');
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    const fetchOrders = useCallback(async () => {
        try {
            setLoading(true);
            const response = await api.getUserOrders(role, page);
            console.log('Orders response:', response); // Debug log
            if (response && response.data) {
                setOrders(response.data.orders || []);
                setTotalPages(response.data.total_pages || 1);
            } else {
                throw new Error('Invalid response format');
            }
        } catch (err) {
            console.error('Error fetching orders:', err);
            setError('Failed to load orders');
            setOrders([]); // Set empty array on error
        } finally {
            setLoading(false);
        }
    }, [role, page]);

    useEffect(() => {
        fetchOrders();
    }, [fetchOrders]);

    const handleStatusUpdate = async (orderId, newStatus) => {
        try {
            await api.updateOrderStatus(orderId, newStatus);
            await fetchOrders();
        } catch (err) {
            setError('Failed to update order status');
        }
    };

    if (loading) return <div>Loading orders...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="orders-container">
            {user.is_seller && (
                <div className="role-toggle">
                    <button
                        onClick={() => setRole('buyer')}
                        className={role === 'buyer' ? 'active' : ''}
                    >
                        My Orders
                    </button>
                    <button
                        onClick={() => setRole('seller')}
                        className={role === 'seller' ? 'active' : ''}
                    >
                        Received Orders
                    </button>
                </div>
            )}

            {Array.isArray(orders) && orders.length > 0 ? (
                orders.map(order => (
                    <div key={order.id} className="order-card">
                        <div className="order-header">
                            <h3>Order #{order.id}</h3>
                            <span className="status">{order.status}</span>
                        </div>

                        {role === 'seller' && (
                            <div className="buyer-info">
                                Buyer: {order.buyer.name}
                            </div>
                        )}

                        <div className="order-items">
                            {order.items.map(item => (
                                <div key={item.id} className="order-item">
                                    <span>{item.name}</span>
                                    <span>x{item.quantity}</span>
                                    <span>${item.price.toFixed(2)}</span>
                                </div>
                            ))}
                        </div>

                        <div className="order-total">
                            Total: ${order.total.toFixed(2)}
                        </div>

                        {role === 'seller' && order.status === 'pending' && (
                            <div className="order-actions">
                                <button onClick={() => handleStatusUpdate(order.id, 'completed')}>
                                    Complete Order
                                </button>
                                <button onClick={() => handleStatusUpdate(order.id, 'cancelled')}>
                                    Cancel Order
                                </button>
                            </div>
                        )}
                    </div>
                ))
            ) : (
                <div className="no-orders">
                    <p>No orders found.</p>
                </div>
            )}

            {Array.isArray(orders) && orders.length > 0 && (
                <div className="pagination">
                    <button
                        onClick={() => setPage(p => p - 1)}
                        disabled={page === 1}
                    >
                        Previous
                    </button>
                    <span>{page} of {totalPages}</span>
                    <button
                        onClick={() => setPage(p => p + 1)}
                        disabled={page === totalPages}
                    >
                        Next
                    </button>
                </div>
            )}
        </div>
    );
};

export default Orders;

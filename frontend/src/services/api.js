import axios from 'axios';
import setupInterceptors from './authInterceptor';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000/api';

const axiosInstance = axios.create({
    baseURL: API_URL,
    timeout: 10000
});

// Apply interceptors
setupInterceptors(axiosInstance);

const api = {
    axiosInstance, // Export axiosInstance for other services

    // Auth
    login: (data) => axiosInstance.post('/login', data),
    register: (data) => axiosInstance.post('/register', {
        email: data.email,
        password: data.password,
        full_name: data.fullname,
        university: data.university
    }),
    logout: () => axiosInstance.post('/logout'),

    // Orders
    createOrder: (items) => axiosInstance.post('/orders', { items }),
    getUserOrders: (role = 'buyer', page = 1) =>
        axiosInstance.get('/user/orders', {
            params: { role, page, per_page: 10 }
        }).then(response => {
            console.log('API response:', response); // Debug log
            return {
                data: {
                    orders: response.data.orders || [],
                    total_pages: response.data.total_pages || 1,
                    current_page: response.data.current_page || 1
                }
            };
        }).catch(error => {
            console.error('API error:', error);
            throw error;
        }),
    updateOrderStatus: (orderId, status) =>
        axiosInstance.put(`/orders/${orderId}/status`, { status }),

    // Cart operations
    addToCart: (productId, quantity) =>
        axiosInstance.post('/cart', {
            productId,
            quantity: parseInt(quantity)
        }).catch(error => {
            console.error('Add to cart error:', error);
            throw error;
        }),
    getCart: () =>
        axiosInstance.get('/cart').catch(error => {
            console.error('Get cart error:', error);
            throw error;
        }),
    updateCartItem: (productId, quantity) =>
        axiosInstance.post('/cart', {
            productId,
            quantity: parseInt(quantity)
        }).catch(error => {
            console.error('Update cart error:', error);
            throw error;
        }),
    removeFromCart: (productId) =>
        axiosInstance.delete(`/cart/${productId}`).catch(error => {
            console.error('Remove from cart error:', error);
            throw error;
        }),
    clearCart: () =>
        axiosInstance.delete('/cart').catch(error => {
            console.error('Clear cart error:', error);
            throw error;
        }),

    // Profile
    getProfile: () => axiosInstance.get('/profile'),
    updateProfile: (data) => axiosInstance.put('/profile/update', data),
    becomeSeller: () => axiosInstance.post('/profile/seller'),

    // Products
    getProducts: (params) => axiosInstance.get('/products', { params }),
    getProduct: (id) => axiosInstance.get(`/products/${id}`),
    createProduct: (data) => axiosInstance.post('/products', data, {
        headers: { 'Content-Type': 'multipart/form-data' }
    }),
    updateProduct: (id, data) => axiosInstance.put(`/products/${id}`, data),
    deleteProduct: (id) => axiosInstance.delete(`/products/${id}`),
};

export default api;
import axios from 'axios';
import setupInterceptors from './authInterceptor';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000/api';

const axiosInstance = axios.create({
    baseURL: API_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
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
    createOrder: (data) => axiosInstance.post('/orders', data),
    getUserOrders: () => axiosInstance.get('/orders/user'),

    // Cart
    addToCart: (productId, quantity) =>
        axiosInstance.post('/cart', { productId, quantity }),
    getCart: () => axiosInstance.get('/cart'),

    // Profile
    getProfile: () => axiosInstance.get('/profile'),
    updateProfile: (data) => axiosInstance.put('/profile/update', data),
    becomeSeller: () => axiosInstance.post('/profile/seller'),
};

export default api;
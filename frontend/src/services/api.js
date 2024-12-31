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
    // Auth
    login: (data) => axiosInstance.post('/login', data),
    register: (data) => axiosInstance.post('/register', {
        email: data.email,
        password: data.password,
        full_name: data.fullname,  // Changed to match backend
        university: data.university
    }),
    logout: () => axiosInstance.post('/logout'),  // Add logout endpoint

    // Products
    getProducts: (page = 1, limit = 10) =>
        axiosInstance.get(`/products?page=${page}&limit=${limit}`),
    getProduct: (id) => axiosInstance.get(`/products/${id}`),

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
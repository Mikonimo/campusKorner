import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const orderApi = {
    createOrder: async (productId) => {
        const response = await axios.post(`${BASE_URL}/orders`, {
            product_id: productId
        }, {
            withCredentials: true
        });
        return response.data;
    },

    getOrder: async (orderId) => {
        const response = await axios.get(`${BASE_URL}/orders/${orderId}`, {
            withCredentials: true
        });
        return response.data;
    },

    updateOrderStatus: async (orderId, status) => {
        const response = await axios.put(`${BASE_URL}/orders/${orderId}/status`, {
            status
        }, {
            withCredentials: true
        });
        return response.data;
    },

    getUserOrders: async (role = 'buyer', page = 1, perPage = 10) => {
        const response = await axios.get(`${BASE_URL}/user/orders`, {
            params: {
                role,
                page,
                per_page: perPage
            },
            withCredentials: true
        });
        return response.data;
    }
};

export default orderApi;

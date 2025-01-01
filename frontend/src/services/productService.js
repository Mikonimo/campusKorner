import api from './api';

const productService = {
    getProducts: (params = {}) => {
        const { page = 1, perPage = 10, search, sort, order } = params;
        const queryParams = new URLSearchParams({
            page,
            per_page: perPage,
            ...(search && { search }),
            ...(sort && { sort }),
            ...(order && { order })
        });
        return api.axiosInstance.get(`/products?${queryParams}`);
    },

    getProduct: (id) =>
        api.axiosInstance.get(`/products/${id}`),

    createProduct: (formData) => {
        // Don't set any Content-Type header, let the browser handle it
        return api.axiosInstance.post('/products', formData, {
            headers: {
                'Accept': 'application/json'
            }
        });
    },

    updateProduct: (id, updateData) =>
        api.axiosInstance.put(`/products/${id}`, updateData),

    deleteProduct: (id) =>
        api.axiosInstance.delete(`/products/${id}`)
};

export default productService;

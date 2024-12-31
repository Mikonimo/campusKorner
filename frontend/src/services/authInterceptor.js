const setupInterceptors = (axiosInstance) => {
    axiosInstance.interceptors.request.use(
        (config) => {
            const token = localStorage.getItem('token');
            if (token) {
                // Ensure token is properly formatted with 'Bearer' prefix
                config.headers.Authorization = token.startsWith('Bearer ') ? token : `Bearer ${token}`;
            }
            return config;
        },
        (error) => Promise.reject(error)
    );

    axiosInstance.interceptors.response.use(
        (response) => response,
        (error) => {
            if (error.response?.status === 401) {
                localStorage.removeItem('token');
                window.location.href = '/login';
            }
            return Promise.reject(error);
        }
    );
};

export default setupInterceptors;
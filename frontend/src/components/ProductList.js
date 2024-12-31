import React, { useState, useEffect } from 'react';
import api from '../services/api';

const ProductList = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [hasMore, setHasMore] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            setLoading(true);
            try {
                const response = await api.getProducts(page);
                const { products, hasMore } = response.data;
                setProducts(prev => page === 1 ? products : [...prev, ...products]);
                setHasMore(hasMore);
            } catch (error) {
                setError(error.response?.data?.message || 'Failed to load products');
            } finally {
                setLoading(false);
            }
        };
        fetchProducts();
    }, [page]);

    const formatPrice = (price) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(price);
    };

    const handleAddToCart = async (productId) => {
        try {
            await api.addToCart(productId, 1);
            // Add cart update logic here
        } catch (error) {
            setError(error.response?.data?.message || 'Failed to add to cart');
        }
    };

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    return (
        <div className="product-container">
            <h1>Available Products</h1>
            {loading && products.length === 0 ? (
                <div className="loading-spinner">Loading products...</div>
            ) : (
                <>
                    <div className="product-grid">
                        {products.length > 0 ? (
                            products.map((product) => (
                                <div key={product.id} className="product-card">
                                    <h3 className="product-title">{product.name}</h3>
                                    <span className="product-category">{product.category}</span>
                                    <p className="product-price">{formatPrice(product.price)}</p>
                                    <button
                                        className="product-button"
                                        onClick={() => handleAddToCart(product.id)}
                                        disabled={loading}
                                    >
                                        Add to Cart
                                    </button>
                                </div>
                            ))
                        ) : (
                            <div className="no-products">No products available</div>
                        )}
                    </div>
                    {hasMore && (
                        <button
                            className="load-more"
                            onClick={() => setPage(p => p + 1)}
                            disabled={loading}
                        >
                            {loading ? 'Loading...' : 'Load More'}
                        </button>
                    )}
                </>
            )}
        </div>
    );
};

export default ProductList;
import React, { useState, useEffect, useCallback } from 'react';
import productService from '../services/productService';
import api from '../services/api';
import './ProductList.css';
import { useNavigate } from 'react-router-dom';

const ProductList = () => {
    const navigate = useNavigate();
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [addingToCart, setAddingToCart] = useState(false);
    const [notification, setNotification] = useState(null);

    const user = JSON.parse(localStorage.getItem('user') || '{}');

    const loadProducts = useCallback(async () => {
        try {
            setLoading(true);
            const response = await productService.getProducts({
                page,
                perPage: 12
            });

            setProducts(response.data.products);
            setTotalPages(response.data.pages);
            setError(null);
        } catch (err) {
            console.error('Failed to load products:', err);
            setError('Failed to load products. Please try again later.');
        } finally {
            setLoading(false);
        }
    }, [page]);

    useEffect(() => {
        loadProducts();
    }, [loadProducts]);

    const handleAddToCart = async (productId) => {
        try {
            setAddingToCart(true);
            await api.addToCart(productId, 1);
            setNotification({
                type: 'success',
                message: 'Product added to cart successfully!'
            });
        } catch (err) {
            setNotification({
                type: 'error',
                message: err.response?.data?.error || 'Failed to add product to cart'
            });
        } finally {
            setAddingToCart(false);
            // Clear notification after 3 seconds
            setTimeout(() => setNotification(null), 3000);
        }
    };

    if (loading) return <div className="loading">Loading products...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="products-container">
            {notification && (
                <div className={`notification ${notification.type}`}>
                    {notification.message}
                </div>
            )}
            <div className="products-grid">
                {products.map(product => (
                    <div key={product.id} className="product-card">
                        <div className="product-image-gallery">
                            {product.images && product.images.length > 0 ? (
                                product.images.map((img, idx) => (
                                    <img
                                        key={idx}
                                        src={img.url}
                                        alt={`${product.name} ${idx + 1}`}
                                        onError={(e) => {
                                            e.target.onerror = null;
                                            e.target.src = 'placeholder-image.png'; // Add a placeholder image
                                        }}
                                    />
                                ))
                            ) : (
                                <div className="no-image">No Image</div>
                            )}
                        </div>
                        <div className="product-info">
                            <h3>{product.name}</h3>
                            <p className="price">${product.price.toFixed(2)}</p>
                            <p className="category">{product.category}</p>
                            <p className="university">{product.university}</p>
                            <p className="seller">Seller: {product.seller.name}</p>
                            {user.id === product.seller.id && (
                                <button
                                    className="edit-product-btn"
                                    onClick={() => navigate(`/products/${product.id}/edit`)}
                                >
                                    Edit
                                </button>
                            )}
                            <button
                                className="add-to-cart-btn"
                                onClick={() => handleAddToCart(product.id)}
                                disabled={addingToCart}
                            >
                                {addingToCart ? 'Adding...' : 'Add to Cart'}
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {totalPages > 1 && (
                <div className="pagination">
                    <button
                        onClick={() => setPage(p => Math.max(1, p - 1))}
                        disabled={page === 1}
                    >
                        Previous
                    </button>
                    <span>Page {page} of {totalPages}</span>
                    <button
                        onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                        disabled={page === totalPages}
                    >
                        Next
                    </button>
                </div>
            )}
        </div>
    );
};

export default ProductList;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import productService from '../services/productService';
import './ProductForm.css';

const AddProduct = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        price: '',
        category: '',
        condition: 'new',
        images: []
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleImageChange = (e) => {
        const files = Array.from(e.target.files);
        setFormData(prev => ({
            ...prev,
            images: files
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const formDataToSend = new FormData();

            // Ensure price is sent as a string
            const priceValue = parseFloat(formData.price).toFixed(2);

            formDataToSend.append('name', formData.name);
            formDataToSend.append('description', formData.description);
            formDataToSend.append('price', priceValue);
            formDataToSend.append('category', formData.category);
            formDataToSend.append('condition', formData.condition);

            // Add each image file individually
            if (formData.images && formData.images.length > 0) {
                for (let i = 0; i < formData.images.length; i++) {
                    formDataToSend.append(`image${i}`, formData.images[i]);
                }
            }

            const response = await productService.createProduct(formDataToSend);
            console.log('Product created:', response);
            navigate('/');
        } catch (err) {
            console.error('Error details:', err);
            setError(err.response?.data?.error || 'Failed to create product');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <div className="product-form-container">
            <h2>Add New Product</h2>
            {error && <div className="error-message">{error}</div>}
            <form onSubmit={handleSubmit} className="product-form" encType="multipart/form-data">
                <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Product Name"
                    required
                />
                <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    placeholder="Description"
                    required
                />
                <input
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    placeholder="Price"
                    step="0.01"
                    required
                />
                <select
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    required
                >
                    <option value="">Select Category</option>
                    <option value="books">Books</option>
                    <option value="electronics">Electronics</option>
                    <option value="furniture">Furniture</option>
                    <option value="clothing">Clothing</option>
                    <option value="appliances">Appliances</option>
                    <option value="kitchen">Kitchen</option>
                    <option value="sports">Sports</option>
                    <option value="beauty">Beauty</option>
                    <option value="health">Health</option>
                    <option value="services">Services</option>
                    <option value="other">Other</option>
                </select>
                <select
                    name="condition"
                    value={formData.condition}
                    onChange={handleChange}
                    required
                >
                    <option value="new">New</option>
                    <option value="like-new">Like New</option>
                    <option value="good">Good</option>
                    <option value="fair">Fair</option>
                    <option value="used">Used</option>
                    <option value="refurbished">Refurbished</option>
                    <option value="open-box">Open Box</option>
                    <option value="damaged">Damaged</option>
                    <option value="defective">Defective</option>
                    <option value="poor">Poor</option>
                </select>
                <input
                    type="file"
                    name="images"
                    onChange={handleImageChange}
                    multiple
                    accept="image/*"
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Creating...' : 'Create Product'}
                </button>
            </form>
        </div>
    );
};

export default AddProduct;

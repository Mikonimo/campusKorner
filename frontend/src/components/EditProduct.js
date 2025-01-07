
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../services/api';
import './ProductForm.css';

const EditProduct = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    category: '',
    condition: 'new'
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const { data } = await api.getProduct(id);
        setFormData({
          name: data.name,
          description: data.description,
          price: String(data.price),
          category: data.category,
          condition: data.condition || 'new'
        });
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to load product');
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await api.updateProduct(id, formData);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update product');
    }
  };

  const handleDelete = async () => {
    try {
      await api.deleteProduct(id);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete product');
    }
  };

  if (loading) return <div>Loading product details...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="product-form-container">
      <h2>Edit Product</h2>
      <form onSubmit={handleUpdate} className="product-form">
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
          {/* ...existing options... */}
          <option value="books">Books</option>
          <option value="electronics">Electronics</option>
          <option value="furniture">Furniture</option>
          {/* ...existing options... */}
        </select>
        <select
          name="condition"
          value={formData.condition}
          onChange={handleChange}
          required
        >
          {/* ...existing options... */}
          <option value="new">New</option>
          <option value="good">Good</option>
          {/* ...existing options... */}
        </select>
        <button type="submit">Update Product</button>
      </form>
      <button onClick={handleDelete} className="delete-btn">
        Delete Product
      </button>
    </div>
  );
};

export default EditProduct;
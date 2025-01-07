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
  const [existingImages, setExistingImages] = useState([]);
  const [newImages, setNewImages] = useState([]);
  const [removedImages, setRemovedImages] = useState([]);

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
        const productImages = data.images || [];
        setExistingImages(productImages);
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

  const handleNewImages = (e) => {
    setNewImages([...e.target.files]);
  };

  const handleRemoveExistingImage = (imageId) => {
    setRemovedImages(prev => [...prev, imageId]);
    setExistingImages(prev => prev.filter(img => img.id !== imageId));
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const fd = new FormData();
      fd.append('name', formData.name);
      fd.append('description', formData.description);
      fd.append('price', formData.price);
      fd.append('category', formData.category);
      fd.append('condition', formData.condition);

      newImages.forEach((file, index) => {
        fd.append(`newImage${index}`, file);
      });

      if (removedImages.length > 0) {
        fd.append('removedImages', JSON.stringify(removedImages));
      }

      await api.updateProduct(id, fd); 
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
      <form onSubmit={handleUpdate} className="product-form" encType="multipart/form-data">
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
          <option value="books">Books</option>
          <option value="electronics">Electronics</option>
          <option value="furniture">Furniture</option>
          <option value="books">Books</option>
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
          <option value="good">Good</option>
          <option value="like-new">Like New</option>
          <option value="fair">Fair</option>
          <option value="used">Used</option>
          <option value="refurbished">Refurbished</option>
          <option value="open-box">Open Box</option>
          <option value="damaged">Damaged</option>
          <option value="defective">Defective</option>
          <option value="poor">Poor</option>
        </select>
        <div className="existing-images">
          {existingImages.map((img) => (
            <div key={img.id} className="existing-image-item">
              <img src={img.url} alt="Existing" />
              <button type="button" onClick={() => handleRemoveExistingImage(img.id)}>
                Remove
              </button>
            </div>
          ))}
        </div>
        <input type="file" multiple accept="image/*" onChange={handleNewImages} />
        <button type="submit">Update Product</button>
      </form>
      <button onClick={handleDelete} className="delete-btn">
        Delete Product
      </button>
    </div>
  );
};

export default EditProduct;
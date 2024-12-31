import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Profile = () => {
    const [profile, setProfile] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        full_name: '',
        university: '',
        bio: '',
        phone_number: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(true);
    const [updateSuccess, setUpdateSuccess] = useState('');

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const response = await api.getProfile();
            if (response.data) {
                setProfile(response.data);
                setFormData({
                    full_name: response.data.full_name || '',
                    university: response.data.university || '',
                    bio: response.data.bio || '',
                    phone_number: response.data.phone_number || ''
                });
            }
        } catch (error) {
            console.error('Profile fetch error:', error);
            setError('Failed to load profile. Please try again.');
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

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await api.updateProfile(formData);
            setUpdateSuccess('Profile updated successfully!');
            setIsEditing(false);
            fetchProfile();
            setTimeout(() => setUpdateSuccess(''), 3000);
        } catch (error) {
            setError(error.response?.data?.message || 'Failed to update profile');
        }
    };

    const handleBecomeSeller = async () => {
        try {
            await api.becomeSeller();
            setUpdateSuccess('Successfully upgraded to seller account!');
            fetchProfile();
        } catch (error) {
            setError(error.response?.data?.message || 'Failed to become seller');
        }
    };

    if (loading) return <div className="loading">Loading profile...</div>;
    if (error) return <div className="error-message">{error}</div>;
    if (!profile) return <div className="error-message">No profile data available</div>;

    return (
        <div className="profile-container">
            {updateSuccess && <div className="success-message">{updateSuccess}</div>}
            {isEditing ? (
                // Edit Form
                <form onSubmit={handleSubmit} className="profile-form">
                    <h2>Edit Profile</h2>
                    <div className="form-group">
                        <label htmlFor="full_name">Full Name</label>
                        <input
                            type="text"
                            id="full_name"
                            name="full_name"
                            value={formData.full_name}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="university">University</label>
                        <input
                            type="text"
                            id="university"
                            name="university"
                            value={formData.university}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="bio">Bio</label>
                        <textarea
                            id="bio"
                            name="bio"
                            value={formData.bio}
                            onChange={handleChange}
                            rows="4"
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="phone_number">Phone Number</label>
                        <input
                            type="tel"
                            id="phone_number"
                            name="phone_number"
                            value={formData.phone_number}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-actions">
                        <button type="submit" className="save-button">Save Changes</button>
                        <button type="button" onClick={() => setIsEditing(false)} className="cancel-button">
                            Cancel
                        </button>
                    </div>
                </form>
            ) : (
                // View Profile
                <div className="profile-view">
                    <h2>Profile</h2>
                    <div className="profile-info">
                        <p><strong>Name:</strong> {profile.full_name}</p>
                        <p><strong>Email:</strong> {profile.email}</p>
                        <p><strong>University:</strong> {profile.university}</p>
                        {profile.bio && <p><strong>Bio:</strong> {profile.bio}</p>}
                        {profile.phone_number && <p><strong>Phone:</strong> {profile.phone_number}</p>}
                        <p><strong>Account Type:</strong> {profile.is_seller ? 'Seller' : 'Buyer'}</p>
                    </div>
                    <div className="profile-actions">
                        <button onClick={() => setIsEditing(true)} className="edit-button">
                            Edit Profile
                        </button>
                        {!profile.is_seller && (
                            <button onClick={handleBecomeSeller} className="seller-button">
                                Become a Seller
                            </button>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Profile;

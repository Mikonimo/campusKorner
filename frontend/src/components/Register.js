import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/register', { email, password });
            alert(response.data.message);
        } catch (error) {
            alert('Registration failed');
        }
    };

    return (
        <form onSubmit={handleRegister}>
            <input type="email" value={email} onChange={(e) =>
                setEmail(e.target.value)} placeholder="Email" required />
            <input type="password" value={password} onChange={(e) =>
                setPassword(e.target.value)} placeholder="Password" required />
        </form>
    );
};

export default Register;

import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1.5000/login', { email, password });
            alert(response.data.message);
        } catch (error) {
            alert('Invalid credentials');
        }
    };

    return (
        <form onSubmit={handleLogin}>
            <input type="email" value={email} onChange={(e) =>
                setEmail(e.target.value)} placeholder="Email" required/>
            <input type="password" value={password} onChange={(e) =>
                setPassword(e.target.value)} placeholder="Password" required/>
        </form>
    );
};

export default Login;

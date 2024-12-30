import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import ProductList from './components/ProductList';

const App = () => (
  <Router>
    <div>
      <nav style={{
        padding: '1rem',
        backgroundColor: '#333',
        color: 'white'
      }}>
        <Link to="/" style={{ color: 'white', marginRight: '1rem' }}>Home</Link>
        <Link to="/register" style={{ color: 'white', marginRight: '1rem' }}>Register</Link>
        <Link to="/login" style={{ color: 'white' }}>Login</Link>
      </nav>
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path='/register' element={<Register />} />
        <Route path='/login' element={<Login />} />
      </Routes>
    </div>
  </Router>
);

export default App;

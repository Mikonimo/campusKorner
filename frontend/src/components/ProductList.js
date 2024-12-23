import React from 'react';

const ProductList = () => {
    const products = [
        { id: 1, name: 'T-shirt', category: 'Clothes', price: '$10'},
        { id: 2, name: 'Laptop', category: 'Gadgets', price: '$300'},
    ];

    return (
        <div>
            {products.map((product) => (
                <div key={product.id}>
                    <h3>{product.name}</h3>
                    <p>{product.category}</p>
                    <p>{product.price}</p>
                </div>
            ))}
        </div>
    );
};

export default ProductList;
#!/usr/bin/env python
"""Product Routes"""
from flask import Blueprint, request, jsonify
from models import Product, ProductImage, db

product_bp = Blueprint('product_bp', __name__)


@product_bp.route('/products', methods=['POST'])
def create_product():
    """
    POST /products
        adds products items
    Return
        - JSON payload
    """
    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=data['category'],
        condition=data.get('condition'),
        seller_id=data['seller_id'],
        university=data['university']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product created', 'product': product.id}), 201

@product_bp.route('/products', methods=['GET'])
def get_products():
    """
    GET /products
        retrieves product items
    Return:
        - JSON payload
    """
    university = request.args.get('university')
    category = request.args.get('category')
    query = Product.query

    if university:
        query = query.filter_by(university=university)
    if category:
        query = query.filter_by(category=category)

    products = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description,
        'category': p.category,
        'university': p.university,
        'status': p.status
    } for p in products]), 200

@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """sumary_line
    GET /products/<int:id>
        retrieves a product with a specific id

    Args:
        id (int): product id
    Return:
        - JSON payload
    """
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'category': product.category,
        'university': product.university,
        'status': product.status
    }), 200

@product_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    """
    PUT /products/<int:id>
        updates a specific product(id)
    Args:
        id (int): product id
    Returns:
        - JSON payload
    """
    product = Product.query.get_or_404(id)
    data = request.get_json()

    for key, value in data.items():
        setattr(product, key, value)

    db.session.commit()
    return jsonify({'message': 'Product updated'}), 200

@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """
    DELETE /products/<int:id>
        deletes a specific produc(id)
    Args:
        id (int): product id
    Returns:
        - JSON payload
    """
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

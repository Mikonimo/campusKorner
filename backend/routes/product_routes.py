#!/usr/bin/env python
"""Product Routes"""
from flask import Blueprint, request, jsonify
from models import Product, ProductImage, db
from routes.auth_routes import token_required
from sqlalchemy import or_

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['POST'])
@token_required
def create_product(current_user):
    """Create a new product"""
    if not current_user.is_seller:
        return jsonify({'error': 'Seller account required'}), 403

    data = request.get_json()
    required_fields = ['name', 'description', 'price', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=data['category'],
        condition=data.get('condition'),
        seller_id=current_user.id,
        university=current_user.university
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product created', 'product': product.id}), 201

@product_bp.route('/products', methods=['GET'])
def get_products():
    """Get products with pagination and search"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        category = request.args.get('category', '')

        query = Product.query.filter(Product.status == 'available')

        if search:
            query = query.filter(or_(
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%')
            ))

        if category:
            query = query.filter(Product.category == category)

        pagination = query.order_by(Product.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False)

        products = [{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'description': p.description,
            'category': p.category,
            'condition': p.condition,
            'university': p.university,
            'status': p.status,
            'created_at': p.created_at.isoformat(),
            'seller': {
                'id': p.seller_id,
                'name': p.seller.full_name,
                'university': p.seller.university
            },
            'images': [{'url': img.image_url, 'is_primary': img.is_primary}
                      for img in p.images]
        } for p in pagination.items]

        return jsonify({
            'products': products,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@product_bp.route('/products/<int:id>', methods=['PUT', 'DELETE'])
@token_required
def modify_product(current_user, id):
    """Modify or delete a product"""
    product = Product.query.get_or_404(id)

    if product.seller_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    if request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'}), 200

    data = request.get_json()
    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)

    db.session.commit()
    return jsonify({'message': 'Product updated'}), 200

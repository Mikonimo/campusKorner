#!/usr/bin/env python
"""Product Routes"""
from flask import Blueprint, request, jsonify
from models import Product, ProductImage, db
from routes.auth_routes import token_required
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import os

product_bp = Blueprint('product_bp', __name__)

# Define upload folder path and ensure it exists
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, '..', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@product_bp.route('/products', methods=['POST'])
@token_required
def create_product(current_user):
    """Create a new product"""
    if not current_user.is_seller:
        return jsonify({'error': 'Seller account required'}), 403

    try:
        # Debug prints
        print("Request content type:", request.content_type)
        print("Form data:", request.form.to_dict())
        print("Files:", request.files.to_dict())

        if not request.form:
            return jsonify({'error': 'No form data received'}), 400

        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')
        condition = request.form.get('condition')

        if not all([name, description, price, category]):
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            price_float = float(price)
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400

        # Create product
        product = Product(
            name=name,
            description=description,
            price=price_float,
            category=category,
            condition=condition,
            seller_id=current_user.id,
            university=current_user.university
        )

        db.session.add(product)
        db.session.commit()  # Commit to get product ID

        # Handle images if present
        if request.files:
            for key in request.files:
                file = request.files[key]
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{product.id}_{key}_{file.filename}")
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)

                    product_image = ProductImage(
                        product_id=product.id,
                        image_url=f"/uploads/{filename}",
                        is_primary=(key == '0')
                    )
                    db.session.add(product_image)

        db.session.commit()
        return jsonify({
            'message': 'Product created successfully',
            'product_id': product.id
        }), 201

    except Exception as e:
        db.session.rollback()
        print("Error creating product:", str(e))  # Debug print
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
                Product.description.ilike(f'%search%')
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

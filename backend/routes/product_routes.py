#!/usr/bin/env python
"""Product Routes"""
from flask import Blueprint, request, jsonify, send_from_directory
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

def get_full_url(path):
    """Helper to get full URL for image paths"""
    if path.startswith('http'):
        return path
    return f"{request.host_url.rstrip('/')}/api{path}"

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
            'images': [{
                'url': get_full_url(img.image_url),
                'is_primary': img.is_primary
            } for img in p.images]
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
        'status': product.status,
        'images': [{
            'id': img.id,
            'url': get_full_url(img.image_url),
            'is_primary': img.is_primary
        } for img in product.images]
    }), 200

@product_bp.route('/products/<int:id>', methods=['PUT', 'DELETE'])
@token_required
def modify_product(current_user, id):
    """Modify or delete a product"""
    product = Product.query.get_or_404(id)
    if product.seller_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    if request.method == 'DELETE':
        # Check if product is part of any orders
        if any(order_item.order_ref.status in ['pending', 'completed']
               for order_item in product.order_items):
            return jsonify({
                'error': 'Cannot delete product that is part of active or completed orders'
            }), 400

        try:
            # Delete related order items for cancelled orders
            for order_item in product.order_items:
                if order_item.order_ref.status == 'cancelled':
                    db.session.delete(order_item)

            # Delete product images
            for image in product.images:
                file_path = os.path.join(UPLOAD_FOLDER, os.path.basename(image.image_url))
                if os.path.exists(file_path):
                    os.remove(file_path)
                db.session.delete(image)

            # Delete the product
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted'}), 200

        except Exception as e:
            db.session.rollback()
            print(f"Error deleting product: {str(e)}")
            return jsonify({'error': 'Failed to delete product'}), 500

    # Handle multipart form data for updates
    print("Request content type:", request.content_type)
    removed_images = request.form.get('removedImages')
    if removed_images:
        removed_list = []
        try:
            removed_list = eval(removed_images)  # or json.loads
        except:
            pass
        for img_id in removed_list:
            img = ProductImage.query.filter_by(id=img_id, product_id=product.id).first()
            if img:
                # Remove file from disk
                file_path = os.path.join(UPLOAD_FOLDER, os.path.basename(img.image_url))
                if os.path.exists(file_path):
                    os.remove(file_path)
                db.session.delete(img)
        db.session.commit()

    # Update product fields
    # (If any form field is missing, the old value remains)
    name = request.form.get('name')
    if name: product.name = name
    description = request.form.get('description')
    if description: product.description = description
    price = request.form.get('price')
    if price:
        try:
            product.price = float(price)
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400
    category = request.form.get('category')
    if category: product.category = category
    condition = request.form.get('condition')
    if condition: product.condition = condition

    # Process newly uploaded images
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
                    is_primary=False  # Or decide your own logic
                )
                db.session.add(product_image)

    db.session.commit()
    return jsonify({'message': 'Product updated'}), 200

@product_bp.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

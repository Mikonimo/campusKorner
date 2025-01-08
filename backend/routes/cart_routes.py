#!/usr/bin/env python
"""Cart Routes"""
from flask import Blueprint, request, jsonify
# Use absolute imports
from models import CartItem, Product, db
from routes.auth_routes import token_required
from sqlalchemy.exc import IntegrityError

__all__ = ['cart_bp']

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/cart', methods=['GET'])
@token_required
def get_cart(current_user):
    try:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'items': [{
                'id': item.id,
                'product_id': item.product_id,
                'name': item.product.name,  # This should now work
                'price': item.product.price,
                'quantity': item.quantity,
                'total': item.product.price * item.quantity
            } for item in cart_items]
        }), 200
    except Exception as e:
        print(f"Error in get_cart: {str(e)}")
        return jsonify({'error': 'Failed to fetch cart items'}), 500

@cart_bp.route('/cart', methods=['POST'])
@token_required
def add_to_cart(current_user):
    """Add or update item in cart"""
    data = request.get_json()

    if not all(k in data for k in ['productId', 'quantity']):
        return jsonify({'error': 'Missing required fields'}), 400

    product_id = data['productId']
    quantity = int(data['quantity'])

    # Check if product exists
    product = Product.query.get_or_404(product_id)

    # Check if product is available
    if product.status != 'available':
        return jsonify({'error': 'Product is not available'}), 400

    # Remove item if quantity is 0
    if quantity == 0:
        CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).delete()
        db.session.commit()
        return jsonify({'message': 'Item removed from cart'}), 200

    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    try:
        if cart_item:
            cart_item.quantity = quantity
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)

        db.session.commit()
        return jsonify({'message': 'Cart updated successfully'}), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to update cart'}), 400

@cart_bp.route('/cart', methods=['DELETE'])
@token_required
def clear_cart(current_user):
    """Clear user's cart"""
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'message': 'Cart cleared successfully'}), 200

@cart_bp.route('/cart/<int:product_id>', methods=['DELETE'])
@token_required
def remove_from_cart(current_user, product_id):
    """Remove specific item from cart"""
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first_or_404()

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}), 200
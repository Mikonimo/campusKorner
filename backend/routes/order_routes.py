#!/usr/bin/env python3
"""Handles Order routes"""
from flask import Blueprint, request, jsonify
from models import Order, Product, OrderItem, db
from routes.auth_routes import token_required

order_bp = Blueprint('order_bp', __name__)


@order_bp.route('/orders', methods=['POST'])
@token_required
def create_order(current_user):
    try:
        data = request.get_json()
        items = data.get('items', [])

        if not items:
            return jsonify({'error': 'No items in order'}), 400

        # Create new order first
        order = Order(buyer_id=current_user.id, status='pending')
        db.session.add(order)
        db.session.flush()  # This gets the order.id before commit

        total_amount = 0
        for item in items:
            product = Product.query.get_or_404(item['id'])
            if product.status != 'available':
                db.session.rollback()
                return jsonify({'error': f'Product {product.name} is not available'}), 400

            # Create order item
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item['quantity'],
                price=product.price
            )
            db.session.add(order_item)
            total_amount += product.price * item['quantity']
            
            # Update product status
            product.status = 'pending'

        db.session.commit()
        return jsonify({
            'message': 'Order created successfully',
            'order_id': order.id,
            'total_amount': total_amount
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Order creation error: {str(e)}")  # Add logging
        return jsonify({'error': 'Failed to create order'}), 500

@order_bp.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        'id': order.id,
        'buyer_id': order.buyer_id,
        'seller_id': order.seller_id,
        'product_id': order.product_id,
        'status': order.status,
        'created_at': order.created_at
    }), 200

@order_bp.route('/orders/<int:id>/status', methods=['PUT'])
@token_required
def update_order_status(current_user, id):
    order = Order.query.get_or_404(id)

    if order.seller_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    if not data.get('status') in ['pending', 'completed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400

    order.status = data['status']
    if order.status == 'completed':
        order.product.status = 'sold'
    elif order.status == 'cancelled':
        order.product.status = 'available'

    db.session.commit()
    return jsonify({'message': 'Order status updated'}), 200

@order_bp.route('/user/orders', methods=['GET'])
@token_required
def get_user_orders(current_user):
    role = request.args.get('role', 'buyer')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Order.query
    if role == 'buyer':
        query = query.filter_by(buyer_id=current_user.id)
    else:
        query = query.filter_by(seller_id=current_user.id)

    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page)

    return jsonify({
        'orders': [{
            'id': o.id,
            'status': o.status,
            'created_at': o.created_at.isoformat(),
            'items': [{
                'id': item.product.id,
                'name': item.product.name,
                'price': item.price,
                'quantity': item.quantity
            } for item in o.items],
            'total': sum(item.price * item.quantity for item in o.items),
            'buyer': {
                'id': o.buyer.id,
                'name': o.buyer.full_name
            } if role == 'seller' else None
        } for o in pagination.items],
        'total_pages': pagination.pages,
        'current_page': page,
        'total_orders': pagination.total
    }), 200

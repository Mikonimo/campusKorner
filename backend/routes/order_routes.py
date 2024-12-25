#!/usr/bin/env python3
"""Handles Order routes"""
from flask import Blueprint, request, jsonify
from models import Order, db

order_bp = Blueprint('order_bp', __name__)


@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(
        buyer_id=data['buyer_id'],
        seller_id=data['seller_id'],
        product_id=data['product_id']
    )
    db.session(order)
    db.session.commit()
    return jsonify({'message': 'Order created', 'order': order.id}), 201

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
def update_order_status(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Order status updated'}), 200

@order_bp.route('/user/orders', methods=['GET'])
def get_user_orders():
    user_id = request.args.get('user_id')
    role = request.args.get('role', 'buyer')

    if role == 'buyer':
        orders = Order.query.filter_by(buyer_id=user_id).all()
    else:
        orders = Order.query.filter_by(seller_id=user_id).all()

    return jsonify([{
        'id': o.id,
        'status': o.status,
        'created_at': o.created_at
    } for o in orders]), 200

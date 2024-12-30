#!/usr/bin/env python3
"""Review Routes"""
from flask import Blueprint, request, jsonify
from sqlalchemy import func  # Add this import
from models import Review, db, Order
from routes.auth_routes import token_required

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/reviews', methods=['POST'])
@token_required
def create_review(current_user):
    data = request.get_json()

    # Validate required fields
    required_fields = ['reviewed_user_id', 'order_id', 'rating']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Validate rating range
    if not 1 <= data['rating'] <= 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    # Check if review already exists
    existing_review = Review.query.filter_by(
        reviewer_id=current_user.id,
        order_id=data['order_id']
    ).first()
    if existing_review:
        return jsonify({'error': 'Review already exists for this order'}), 400

    # Verify order exists and belongs to reviewer
    order = Order.query.get_or_404(data['order_id'])
    if order.buyer_id != current_user.id:
        return jsonify({'error': 'Unauthorized to review this order'}), 403

    review = Review(
        reviewer_id=current_user.id,
        reviewed_user_id=data['reviewed_user_id'],
        order_id=data['order_id'],
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Review created', 'review_id': review.id}), 201

@review_bp.route('/reviews/user/<int:user_id>', methods=['GET'])
def get_user_reviews(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Review.query.filter_by(reviewed_user_id=user_id)\
        .order_by(Review.created_at.desc())\
        .paginate(page=page, per_page=per_page)

    avg_rating = Review.query.filter_by(reviewed_user_id=user_id)\
        .with_entities(func.avg(Review.rating)).scalar() or 0

    return jsonify({
        'reviews': [{
            'id': r.id,
            'rating': r.rating,
            'comment': r.comment,
            'reviewer_id': r.reviewer_id,
            'reviewer_name': r.reviewer.full_name if r.reviewer else None,
            'created_at': r.created_at.isoformat(),
            'order_id': r.order_id
        } for r in pagination.items],
        'total_pages': pagination.pages,
        'current_page': page,
        'total_reviews': pagination.total,
        'average_rating': float(round(avg_rating, 2))
    }), 200

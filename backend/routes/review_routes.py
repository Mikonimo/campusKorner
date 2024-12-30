#!/usr/bin/env python3
"""Review Routes"""
from flask import Blueprint, request, jsonify
from models import Review, db
from routes.auth_routes import token_required

review_bp = Blueprint('review_bp', __name__)


@review_bp.route('/reviews', methods=['POST'])
@token_required
def create_review(current_user):
    data = request.get_json()
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


@review_bp.route('/reviews/user/<int:user_id', methods=['GET'])
def get_user_reviews(user_id):
    reviews = Review.query.filter_by(reviewed_user_id=user_id).all()
    return jsonify([{
        'id': r.id,
        'rating': r.rating,
        'comment': r.comment,
        'reviewer_id': r.reviewer_id,
        'created_at': r.created_at
    } for r in reviews]), 200

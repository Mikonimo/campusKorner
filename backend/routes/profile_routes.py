#!/usr/bin/env python3
"""Profile Routes"""
from flask import Blueprint, request, jsonify
from models import User, db
from routes.auth_routes import token_required

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get user profile"""
    return jsonify({
        'id': current_user.id,
        'email': current_user.email,
        'full_name': current_user.full_name,
        'university': current_user.university,
        'is_seller': current_user.is_seller,
        'is_verified': current_user.is_verified
    })

@profile_bp.route('/profile/update', methods='PUT')
@token_required
def update_profile(current_user):
    data = request.get_json()
    for key, value in data.items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)
    db.session.commit()
    return jsonify({'message': 'Profile updated'}), 200



@profile_bp.route('/profile/seller', methods=['POST'])
@token_required
def become_seller(current_user):
    current_user.is_seller = True
    db.session.commit()
    return jsonify({'message': 'Upgraded to seller account'}), 200
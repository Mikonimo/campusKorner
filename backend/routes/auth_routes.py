#!/usr/bin/env python3
"""Routes for authentication (login, register)"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
import jwt
from datetime import datetime, timedelta
from functools import wraps
import logging

auth_bp = Blueprint('auth_bp', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'message': 'Invalid token format'}), 401
        try:
            token = token.split()[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                raise ValueError('User not found')
        except Exception as e:
            return jsonify({'message': 'Invalid token', 'error': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    POST /register
        register a new user
    Returns:
        - JSON payload"""
    data = request.json
    required_fields = ['email', 'password', 'full_name', 'university']

    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 409

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(
        email=data['email'],
        password=hashed_password,
        full_name=data['full_name'],
        university=data['university']
    )
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({
        'user_id': str(new_user.id),
        'exp': str(datetime.utcnow() + timedelta(days=1))
    },'your-secret-key', algorithm="HS256")

    return jsonify({
        'message': 'User registered successfully!',
        'token': token,
        'user': {
            'id': new_user.id,
            'email': new_user.email,
            'full_name': new_user.full_name,
            'university': new_user.university
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    POST /Login
        login a user
    Returns:
        - JSON payload"""
    try:
        data = request.json
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Missing email or password'}), 400

        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401

        exp_time = datetime.utcnow() + timedelta(days=1)
        token_payload = {
            'user_id': str(user.id),
            'exp': int(exp_time.timestamp()),
            'iat': int(datetime.utcnow().timestamp())
        }

        token = jwt.encode(
            token_payload,
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )

        return jsonify({
            'message': 'Login successful!',
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'university': user.university
            }
        }), 200
    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({'message': 'An error occurred'}), 500


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({'message': 'Logout successful'}), 200
#!/usr/bin/env python3
"""Routes for authentication (login, register)"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    """
    POST /register
        register a new user
    Returns:
        - JSON payload"""
    data = request.json
    hashed_password = generate_password_hash(data['password'], methods='sha256')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'})

@auth.route('/login', methods=['POST'])
def login():
    """
    POST /Login
        login a user
    Returns:
        - JSON payload"""
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful!'})
    return jsonify({'message': 'Invalid credentials'}), 401

#!/usr/bin/env python3
"""Category Routes"""
from flask import Blueprint, jsonify, request
from models import Category, db
from routes.auth_routes import token_required

category_bp = Blueprint('category_bp', __name__)


@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in categories]), 200


@category_bp.route('/categories', methods=['POST'])
@token_required
def create_category(current_user):
    data = request.get_json()
    category = Category(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created', 'category_id': category.id}), 201

#!/usr/bin/env python3
"""Category Routes"""
from flask import Blueprint, jsonify, request
from models import Category, db
from routes.auth_routes import token_required

category_bp = Blueprint('category_bp', __name__)


@category_bp.route('/categories', methods=['GET'])
def get_categories():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = Category.query.paginate(page=page, per_page=per_page)

    return jsonify({
        'categories': [{
            'id': c.id,
            'name': c.name,
            'description': c.description
        } for c in pagination.items],
        'total_pages': pagination.pages,
        'current_page': page,
        'total_categories': pagination.total
    }), 200


@category_bp.route('/categories', methods=['POST'])
@token_required
def create_category(current_user):
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400

    # Check for duplicate category
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category already exists'}), 400

    category = Category(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created', 'category_id': category.id}), 201


@category_bp.route('/categories/<int:id>', methods=['PUT', 'DELETE'])
@token_required
def manage_category(current_user, id):
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    category = Category.query.get_or_404(id)

    if request.method == 'DELETE':
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted'}), 200

    data = request.get_json()
    if 'name' in data:
        existing = Category.query.filter_by(name=data['name']).first()
        if existing and existing.id != id:
            return jsonify({'error': 'Category name already exists'}), 400

    for key in ['name', 'description']:
        if key in data:
            setattr(category, key, data[key])

    db.session.commit()
    return jsonify({'message': 'Category updated'}), 200

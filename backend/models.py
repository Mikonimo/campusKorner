#!/usr/bin/env python3
"""Database Models e.g., User, Product"""
from extensions import db
from datetime import datetime
# import Datetime


class User(db.Model):
    """User database model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    university = db.Column(db.String(120), nullable=False)
    is_seller = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(20))
    profile_image = db.Column(db.String(255))
    # created_at = db.Column(Datetime, default=datetime.utcnow)

    # Relationships
    products = db.relationship('Product', backref='')

    def __repr__(self):
        """Representation fo the Class"""
        return f'<User {self.email}>'


class Product(db.Model):
    """Product database model"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50))  # New, Used
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    university = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='available')  # available, sold
    # created_at = db.Column(db.Datetime, default=datetime.utcnow)
    # updated_at = db.Column(Datetime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships

    def __repr__(self):
        return f'<Product {self.name}>'


class ProductImage(db.Model):
    """Product Images database model"""
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    # created_at = db.Column(db.Datetime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ProducImage {self.image_url}>'


class Order(db.Model):
    """Order database model"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, completed, cancelled
    # created_at = db.Column(db.Datetime, default=datetime.utcnow)
    # updated_at = db.Column(db.Datetime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.id}>'


class Review(db.Model):
    """Review database model"""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviewed_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 1-5 stars
    comment = db.Column(db.Text)
    # created_at = db.Column(db.Datetime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.id}>'


class Category(db.Model):
    """Category database model"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Category {self.name}>'

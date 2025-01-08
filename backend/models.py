#!/usr/bin/env python3
"""Database Models e.g., User, Product"""
from extensions import db
from datetime import datetime
from sqlalchemy import DateTime


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
    created_at = db.Column(DateTime, default=datetime.utcnow)

    # Relationships
    products = db.relationship('Product', backref='seller', lazy=True)
    orders_as_buyer = db.relationship('Order', backref='buyer', lazy=True, foreign_keys='Order.buyer_id')
    cart_items = db.relationship(
        'CartItem',
        backref=db.backref('user_ref', lazy=True),
        lazy=True
    )

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
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship(
        'OrderItem',
        backref=db.backref('product_ref', lazy=True),
        lazy=True
    )
    cart_items = db.relationship(
        'CartItem',
        backref=db.backref('product_ref', lazy=True),
        lazy=True
    )

    @property
    def orders(self):
        """Get all orders containing this product"""
        return [item.order for item in self.order_items]

    def __repr__(self):
        return f'<Product {self.name}>'


class ProductImage(db.Model):
    """Product Images database model"""
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ProducImage {self.image_url}>'


class Order(db.Model):
    """Order database model"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = db.relationship(
        'OrderItem',
        backref=db.backref('order_ref', lazy=True),
        lazy=True,
        cascade='all, delete-orphan'
    )

    @property
    def seller_id(self):
        """Get seller ID from the first item in the order"""
        if self.items and self.items[0].product_ref:
            return self.items[0].product_ref.seller_id
        return None

    @property
    def seller(self):
        if self.items and self.items[0].product_ref:
            return self.items[0].product_ref.seller
        return None

    def __repr__(self):
        return f'<Order {self.id}>'


# class Review(db.Model):
#   """Review database model"""
#    __tablename__ = 'reviews'
#
#   id = db.Column(db.Integer, primary_key=True)
#
#   reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#    reviewed_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
#    rating = db.Column(db.Integer, nullable=False) # 1-5 stars
#    comment = db.Column(db.Text)
#    created_at = db.Column(DateTime, default=datetime.utcnow)
#
#    def __repr__(self):
#       return f'<Review {self.id}>'


class Category(db.Model):
    """Category database model"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Category {self.name}>'


class CartItem(db.Model):
    """Cart Item database model"""
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Keep only the product relationship
    product = db.relationship(
        'Product',
        backref=db.backref('cart_references', lazy=True),
        lazy=True
    )

    def __repr__(self):
        return f'<CartItem user_id={self.user_id} product_id={self.product_id}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at time of purchase

    # Remove the direct relationship since it's handled by the backref
    # from Product.order_items

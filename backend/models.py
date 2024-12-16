#!/usr/bin/env python3
"""Database Models e.g., User, Product"""
from app import db


class User(db.Model):
    """User database model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        """Representation fo the Class"""
        return f'<User {self.email}>'

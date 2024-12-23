#!/usr/bin/env python3
"""The main entry point for the Flask application
initializes the app and sets configurations"""
from flask import Flask
from flask_cors import CORS
from extensions import db, migrate
from models import User, Product
import click


def create_app():
    """Initializes Flask App"""
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'mysql+pymysql://mikonimo:8a3k5r13@localhost/campuskorner'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    @app.cli.command("create-db")
    def create_db():
        """Create the database schema"""
        db.create_all()
        click.echo("Database schema created!")

    with app.app_context():
        from routes import init_routes
        init_routes(app)

    return app

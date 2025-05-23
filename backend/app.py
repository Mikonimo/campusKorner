#!/usr/bin/env python3
"""The main entry point for the Flask application
initializes the app and sets configurations"""
from flask import Flask
from flask_cors import CORS
from extensions import db, migrate
import click


def create_app():
    """Initializes Flask App"""
    app = Flask(__name__)
    CORS(app)

    # Load configuration before other initializations
    app.config.from_object('config')

    # Remove these lines since they're now in config.py
    # app.config['SQLALCHEMY_DATABASE_URI'] = ...
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = ...

    db.init_app(app)
    migrate.init_app(app, db)

    @app.cli.command("create-db")
    def create_db():
        """Create the database schema"""
        db.create_all()
        click.echo("Database schema created!")

    @app.cli.command("drop-db")
    def drop_db():
        """Drop the database schema"""
        db.drop_all()
        click.echo("Database schema dropped!")

    with app.app_context():
        from routes import init_routes
        init_routes(app)
        db.create_all()

    return app

#!/usr/bin/env python3
"""Initialize routes"""
from .auth_routes import auth


def init_routes(app):
    app.register_blueprint(auth)

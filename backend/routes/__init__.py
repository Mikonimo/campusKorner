#!/usr/bin/env python3
"""Initialize routes"""

def init_routes(app):
    """Initialize all blueprints"""
    # Import blueprints inside the function to avoid circular imports
    from .auth_routes import auth_bp
    from .order_routes import order_bp
    from .product_routes import product_bp
    from .category_routes import category_bp
    from .review_routes import review_bp
    from .profile_routes import profile_bp
    from .cart_routes import cart_bp

    # Register blueprints
    blueprints = [
        auth_bp,
        product_bp,
        order_bp,
        category_bp,
        review_bp,
        profile_bp,
        cart_bp
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix='/api')

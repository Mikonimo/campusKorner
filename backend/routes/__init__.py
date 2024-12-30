#!/usr/bin/env python3
"""Initialize routes"""


def init_routes(app):
    from .auth_routes import auth_bp
    from .order_routes import order_bp
    from .product_routes import product_bp
    from .category_routes import category_bp
    from .review_routes import review_bp
    from .profile_routes import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(profile_bp)

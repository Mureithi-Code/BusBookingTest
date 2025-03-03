import os
from flask import Flask, request, current_app
from app.extensions import db, jwt, cors, bcrypt
from flask_migrate import Migrate
from app.config import get_config
from app.routes import register_routes

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Load Configuration
    app.config.from_object(get_config())

    # Enable CORS
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    # Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register API Namespaces
    register_routes(app)

    # Import and register namespaces (if needed)
    from app.routes.auth_routes import auth_ns
    from app.routes.admin_routes import admin_ns
    from app.routes.customer_routes import customer_ns
    from app.routes.driver_routes import driver_ns

    # ✅ Add global request logging for better debugging
    @app.before_request
    def log_request():
        current_app.logger.info(f'📥 Incoming {request.method} request to {request.path}')
        current_app.logger.info(f'🔐 Headers: {dict(request.headers)}')

        # Log request body for POST, PUT, PATCH
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                current_app.logger.info(f'📦 Request Body: {request.get_json()}')
            except Exception:
                current_app.logger.info(f'📦 Request Body: (unavailable)')

    return app

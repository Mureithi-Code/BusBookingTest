import os
from flask import Flask
from app.extensions import db, jwt, cors, bcrypt  # Use existing instances
from flask_migrate import Migrate  # Add Migrate
from app.config import Config

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

    # Load Configuration
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)  # Use `cors` from extensions.py
    bcrypt.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)  # ✅ Add this

    # Register Blueprints (Routes)
    from app.routes.admin_routes import admin_bp
    from app.routes.driver_routes import driver_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(driver_bp, url_prefix='/driver')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

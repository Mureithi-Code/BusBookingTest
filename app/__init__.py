import os
from flask import Flask
from app.extensions import db, jwt, cors, bcrypt  # Use existing instances
from flask_migrate import Migrate  # Add Migrate
from app.config import Config
from app.routes import register_routes

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    
    # Load Configuration
    app.config.from_object(Config)
    
    #Enable CORS
    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:3000"}})


    # Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)  # Use `cors` from extensions.py
    bcrypt.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)  # ✅ Add this
    
    # Register API Namespaces
    register_routes(app)  

    # Import and register namespaces
    from app.routes.auth_routes import auth_ns
    from app.routes.admin_routes import admin_ns
    from app.routes.customer_routes import customer_ns
    from app.routes.driver_routes import driver_ns

    return app

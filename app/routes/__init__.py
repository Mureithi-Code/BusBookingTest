from flask import Blueprint

# Define blueprints
admin_bp = Blueprint('admin', __name__)
driver_bp = Blueprint('driver', __name__)
customer_bp = Blueprint('customer', __name__)
auth_bp = Blueprint('auth', __name__)

# Import routes
from app.routes import admin_routes, driver_routes, customer_routes, auth_routes

from flask_restx import Api

# Import Namespaces
from app.routes.auth_routes import auth_ns
from app.routes.admin_routes import admin_ns
from app.routes.customer_routes import customer_ns
from app.routes.driver_routes import driver_ns

# ✅ Initialize API globally to prevent duplicate registration
api = Api(
    title="Bus Booking API",
    version="1.0",
    description="API documentation for Bus Booking System",
    doc="/swagger"
)

# ✅ Add namespaces once
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(admin_ns, path="/admin")
api.add_namespace(customer_ns, path="/customer")
api.add_namespace(driver_ns, path="/driver")

def register_routes(app):
    """Attach API to the Flask app."""
    if not hasattr(app, "api_initialized"):  # ✅ Prevent duplicate registration
        api.init_app(app)
        app.api_initialized = True
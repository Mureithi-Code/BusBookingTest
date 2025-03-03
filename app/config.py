import os

class Config:
    """Base configuration class."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'your_email@example.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your_email_password')
    DEBUG = False  # Default to False, override in subclass if needed


class DevelopmentConfig(Config):
    """Development configuration (local)."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'LOCAL_DATABASE_URI',  # Local DB connection string
        'postgresql://postgres:your_local_password@localhost/busbooking_db'  # Fallback if env var missing
    )


class ProductionConfig(Config):
    """Production configuration (Render)."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',  # Use the DATABASE_URL provided by Render
        'postgresql://shepherd:2gNFHwMhD8dEjw2oAXNDj9gARUQ6RJCC@dpg-cuq7piqn91rc73ar9mo0-a.oregon-postgres.render.com:5432/bus_booking_db_4xim?sslmode=require'
    )


# Helper function to choose config based on FLASK_ENV
def get_config():
    flask_env = os.getenv('FLASK_ENV', 'development').lower()

    if flask_env == 'production':
        return ProductionConfig
    else:
        return DevelopmentConfig

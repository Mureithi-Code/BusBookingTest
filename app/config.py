import os

class Config:
    """Base configuration class."""
    
    # Secret Keys
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'postgresql://shepherd:2gNFHwMhD8dEjw2oAXNDj9gARUQ6RJCC@dpg-cuq7piqn91rc73ar9mo0-a.oregon-postgres.render.com:5432/bus_booking_db_4xim?sslmode=require'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS Configuration
    CORS_HEADERS = 'Content-Type'

    # Email Configuration (Optional)
    EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'your_email@example.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your_email_password')

    # Other Configurations
    DEBUG = True  # Set to False in production

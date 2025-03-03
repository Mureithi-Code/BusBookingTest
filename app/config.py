import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'your_email@example.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your_email_password')
    DEBUG = False  # Default to False, override in subclass if needed

    @staticmethod
    def get_database_uri():
        database_uri = os.getenv('DATABASE_URI')
        if not database_uri:
            raise RuntimeError("DATABASE_URI environment variable is required but not set.")
        return database_uri


class DevelopmentConfig(Config):
    """Development configuration (local)."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()


class ProductionConfig(Config):
    """Production configuration (Render)."""
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()


# Helper function to choose config based on FLASK_ENV
def get_config():
    flask_env = os.getenv('FLASK_ENV', 'development').lower()

    if flask_env == 'production':
        return ProductionConfig
    else:
        return DevelopmentConfig

import sys
import os
import logging
from dotenv import load_dotenv

load_dotenv()
print(f"✅ Debug Check - DATABASE_URI = {os.getenv('DATABASE_URI')}")

logging.basicConfig(level=logging.INFO)

# Ensure the busbooking directory is in the system path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from app import create_app
from app.extensions import db
from flask_migrate import Migrate
# Create the application instance

load_dotenv()
app = create_app()

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.app(debug=True)

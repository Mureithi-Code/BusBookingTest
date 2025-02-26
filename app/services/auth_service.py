from app.extensions import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token
from flask import jsonify
from flask import current_app
from werkzeug.security import generate_password_hash



class AuthService:
    @staticmethod
    def register(data):
        existing_user = User.query.filter_by(email=data.get('email')).first()
        if existing_user:
            return {"error": "User with this email already exists"}, 400
        
        # ✅ Ensure password is hashed correctly
        hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        
        new_user = User(
            name=data.get('name'), 
            email=data.get('email'), 
            password_hash=hashed_password, 
            role=data.get('role')
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User registered successfully"}, 201
        except Exception as e:
            current_app.logger.error(f"Error creating user: {e}")  # Log the error
            db.session.rollback()
            return {"error": "Internal server error"}, 500 
        
    @staticmethod
    def login(data):
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            token = create_access_token(identity=user.id)
            return jsonify({"token": token, "role": user.role})
        return jsonify({"error": "Invalid credentials"}), 401

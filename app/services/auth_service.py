from app.extensions import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token
from flask import jsonify, current_app


class AuthService:

    @staticmethod
    def register(data):
        existing_user = User.query.filter_by(email=data.get('email')).first()
        if existing_user:
            return {"error": "User with this email already exists"}, 400

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
            current_app.logger.error(f"Error creating user: {e}")
            db.session.rollback()
            return {"error": "Internal server error"}, 500

    @staticmethod
    def login(data):
        from flask import current_app
        current_app.logger.info(f'🔐 Login attempt for email: {data["email"]}')
        
        user = User.query.filter_by(email=data['email']).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
            current_app.logger.warning(f"Failed login attempt for email: {data['email']}")
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=str(user.id))
        current_app.logger.info(f'✅ Login successful for {user.email} (ID: {user.id}) - Token issued')

        # Base response for all users
        response = {
            "token": token,
            "role": user.role
        }

        # Extra data for drivers
        if user.role == "Driver":
            response["driver_id"] = user.id
            response["name"] = user.name  # Optional, can be removed if not needed

        current_app.logger.info(f'🔄 Returning login response: {response}')
        return jsonify(response)

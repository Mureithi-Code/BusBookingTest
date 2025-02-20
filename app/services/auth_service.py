from app.extensions import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token
from flask import jsonify

class AuthService:
    @staticmethod
    def register(data):
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(name=data['name'], email=data['email'], password_hash=hashed_password, role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201

    @staticmethod
    def login(data):
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            token = create_access_token(identity=user.id)
            return jsonify({"token": token, "role": user.role})
        return jsonify({"error": "Invalid credentials"}), 401

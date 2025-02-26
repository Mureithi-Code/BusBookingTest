from flask_restx import Namespace, Resource
from flask import request
from app.services.auth_service import AuthService

auth_ns = Namespace("Auth", description="Authentication Endpoints")

@auth_ns.route("/register")
class Register(Resource):
    def post(self):
        """Register a new user"""
        data = request.get_json()
        response, status_code = AuthService.register(data)
        return response, status_code

@auth_ns.route("/login")
class Login(Resource):
    def post(self):
        """User login"""
        data = request.get_json()
        return AuthService.login(data)

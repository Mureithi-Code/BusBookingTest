from flask_restx import Namespace, Resource
from flask import request, current_app
from app.services.auth_service import AuthService

auth_ns = Namespace("Auth", description="Authentication Endpoints")

@auth_ns.route("/register")
class Register(Resource):
    def post(self):
        """Register a new user"""
        data = request.get_json()
        current_app.logger.info(f"Register request received for email: {data.get('email')}")
        response, status_code = AuthService.register(data)
        return response, status_code


@auth_ns.route("/login")
class Login(Resource):
    def post(self):
        """User login"""
        data = request.get_json()
        current_app.logger.info(f"Login attempt for email: {data.get('email')}")
        return AuthService.login(data)

from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.admin_service import AdminService

# Namespace for Swagger documentation
admin_ns = Namespace("Admin", description="Admin Management Endpoints")

@admin_ns.route("/buses")
class GetAllBuses(Resource):
    @jwt_required()
    def get(self):
        """Get all buses (assigned and unassigned)"""
        response, status = AdminService.get_all_buses()
        return response, status

@admin_ns.route("/routes")
class GetAllRoutes(Resource):
    @jwt_required()
    def get(self):
        """Get all routes (assigned and unassigned)"""
        response, status = AdminService.get_all_routes()
        return response, status

@admin_ns.route("/drivers")
class GetAllDrivers(Resource):
    @jwt_required()
    def get(self):
        """Get all drivers"""
        response, status = AdminService.get_all_drivers()
        return response, status

@admin_ns.route("/remove_driver/<int:driver_id>")
class RemoveDriver(Resource):
    @jwt_required()
    def delete(self, driver_id):
        """Remove a driver (also unassigns buses & routes)"""
        response, status = AdminService.remove_driver(driver_id)
        return response, status

@admin_ns.route("/cancel_route/<int:route_id>")
class CancelRoute(Resource):
    @jwt_required()
    def delete(self, route_id):
        """Cancel a route"""
        response, status = AdminService.cancel_route(route_id)
        return response, status

@admin_ns.route("/messages")
class GetAllMessages(Resource):
    @jwt_required()
    def get(self):
        """Get all messages between customers and admin"""
        response, status = AdminService.get_all_messages()
        return response, status

@admin_ns.route("/reply_to_message/<int:message_id>")
class ReplyToMessage(Resource):
    @jwt_required()
    def post(self, message_id):
        """Reply to a message from a customer"""
        data = request.get_json()
        data['sender_id'] = get_jwt_identity()  # Admin sending reply
        response, status = AdminService.reply_to_message(message_id, data)
        return response, status

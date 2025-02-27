from flask_restx import Namespace, Resource
from flask import request
from app.services.admin_service import AdminService

# Define Namespace for Swagger documentation
admin_ns = Namespace("Admin", description="Admin Management Endpoints")

@admin_ns.route("/remove_driver/<int:driver_id>")
class RemoveDriver(Resource):
    def delete(self, driver_id):
        """Remove a driver by ID"""
        response, status = AdminService.remove_driver(driver_id)
        return response, status 
    
@admin_ns.route("/cancel_route/<int:route_id>")
class CancelRoute(Resource):
    def put(self, route_id):
        """Cancel a bus route by ID"""
        return AdminService.cancel_route(route_id)

@admin_ns.route("/reply_message/<int:message_id>")
class ReplyMessage(Resource):
    def post(self, message_id):
        """Reply to a customer message"""
        data = request.get_json()
        return AdminService.reply_message(message_id, data)
    
@admin_ns.route("/drivers")
class DriverList(Resource):
    def get(self):
        """Get all drivers"""
        return AdminService.get_all_drivers()

@admin_ns.route("/routes")
class RouteList(Resource):
    def get(self):
        """Get all routes"""
        return AdminService.get_all_routes()

@admin_ns.route("/messages")
class MessageList(Resource):
    def get(self):
        """Get all customer messages"""
        return AdminService.get_all_messages()


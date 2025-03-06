from flask_restx import Namespace, Resource
from flask import request
from app.services.admin_service import AdminService

admin_ns = Namespace("Admin", description="Admin Management Endpoints")

@admin_ns.route("/buses")
class AdminBuses(Resource):
    def get(self):
        """Get all buses (assigned & unassigned)"""
        response, status = AdminService.get_all_buses()
        return response, status

@admin_ns.route("/routes")
class AdminRoutes(Resource):
    def get(self):
        """Get all routes (assigned & unassigned)"""
        response, status = AdminService.get_all_routes()
        return response, status

@admin_ns.route("/drivers")
class AdminDrivers(Resource):
    def get(self):
        """Get all drivers"""
        response, status = AdminService.get_all_drivers()
        return response, status

@admin_ns.route("/remove_driver/<int:driver_id>")
class RemoveDriver(Resource):
    def delete(self, driver_id):
        """Remove a driver by ID"""
        response, status = AdminService.remove_driver(driver_id)
        return response, status

@admin_ns.route("/cancel_route/<int:route_id>")
class CancelRoute(Resource):
    def delete(self, route_id):
        """Cancel a route by ID"""
        response, status = AdminService.cancel_route(route_id)
        return response, status

@admin_ns.route("/messages")
class AdminMessages(Resource):
    def get(self):
        """View all messages from customers"""
        response, status = AdminService.get_all_messages()
        return response, status

@admin_ns.route("/reply_message/<int:message_id>")
class ReplyMessage(Resource):
    def post(self, message_id):
        """Reply to a customer message"""
        data = request.get_json()
        response, status = AdminService.reply_to_message(message_id, data)
        return response, status

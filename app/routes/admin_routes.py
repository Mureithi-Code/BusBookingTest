from flask import Blueprint, request
from app.services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/remove_driver/<int:driver_id>', methods=['DELETE'])
def remove_driver(driver_id):
    return AdminService.remove_driver(driver_id)

@admin_bp.route('/cancel_route/<int:route_id>', methods=['PUT'])
def cancel_route(route_id):
    return AdminService.cancel_route(route_id)

@admin_bp.route('/reply_message/<int:message_id>', methods=['POST'])
def reply_message(message_id):
    data = request.get_json()
    return AdminService.reply_message(message_id, data)

from flask import Blueprint, request
from app.services.driver_service import DriverService

driver_bp = Blueprint('driver', __name__)

@driver_bp.route('/add_bus', methods=['POST'])
def add_bus():
    data = request.get_json()
    return DriverService.add_bus(data)

@driver_bp.route('/pick_route', methods=['PUT'])
def pick_route():
    data = request.get_json()
    return DriverService.pick_route(data)

@driver_bp.route('/assign_cost/<int:bus_id>', methods=['PUT'])
def assign_cost(bus_id):
    data = request.get_json()
    return DriverService.assign_cost(bus_id, data)

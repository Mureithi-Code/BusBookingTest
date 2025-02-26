from flask_restx import Namespace, Resource
from flask import request
from app.services.driver_service import DriverService

# Define Namespace for Swagger documentation
driver_ns = Namespace("Driver", description="Driver Bus Management Endpoints")

@driver_ns.route("/add_bus")
class AddBus(Resource):
    def post(self):
        """Add a new bus"""
        data = request.get_json()
        return DriverService.add_bus(data)

@driver_ns.route("/pick_route")
class PickRoute(Resource):
    def put(self):
        """Pick and assign a route for a bus"""
        data = request.get_json()
        return DriverService.pick_route(data)

@driver_ns.route("/assign_cost/<int:bus_id>")
class AssignCost(Resource):
    def put(self, bus_id):
        """Assign cost to a bus by bus ID"""
        data = request.get_json()
        return DriverService.assign_cost(bus_id, data)

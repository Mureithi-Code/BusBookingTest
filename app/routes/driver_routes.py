from flask_restx import Namespace, Resource
from flask import request
from app.services.driver_service import DriverService

driver_ns = Namespace("Driver", description="Driver Bus Management Endpoints")

@driver_ns.route("/add_bus")
class AddBus(Resource):
    def post(self):
        data = request.get_json()
        return DriverService.add_bus(data)

@driver_ns.route("/pick_route")
class PickRoute(Resource):
    def put(self):
        data = request.get_json()
        return DriverService.pick_route(data)

@driver_ns.route("/assign_cost/<int:bus_id>")
class AssignCost(Resource):
    def put(self, bus_id):
        data = request.get_json()
        return DriverService.assign_cost(bus_id, data)

@driver_ns.route("/buses/<int:driver_id>")
class DriverBuses(Resource):
    def get(self, driver_id):
        return DriverService.get_driver_buses(driver_id)

@driver_ns.route("/update_bus/<int:bus_id>")
class UpdateBus(Resource):
    def put(self, bus_id):
        data = request.get_json()
        return DriverService.update_bus(bus_id, data)

@driver_ns.route("/remove_bus/<int:bus_id>")
class RemoveBus(Resource):
    def delete(self, bus_id):
        return DriverService.remove_bus(bus_id)

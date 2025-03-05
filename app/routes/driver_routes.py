from flask_restx import Namespace, Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.driver_service import DriverService
from app.utils.response import ResponseHandler  # Correct import from response.py

driver_ns = Namespace("Driver", description="Driver Dashboard Endpoints")

@driver_ns.route("/routes")
class DriverRoutes(Resource):
    @jwt_required()
    def post(self):
        current_app.logger.info('🟡 [DRIVER ROUTE] POST /driver/routes called.')
        data = request.get_json()
        driver_id = get_jwt_identity()

        response, status = DriverService.create_route(driver_id, data)
        return response, status

    @jwt_required()
    def get(self):
        current_app.logger.info('🟡 [DRIVER ROUTE] GET /driver/routes called.')
        driver_id = get_jwt_identity()

        result = DriverService.get_driver_routes(driver_id)
        return ResponseHandler.success("Routes fetched successfully", result)


@driver_ns.route("/buses")
class DriverBuses(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        driver_id = get_jwt_identity()

        result = DriverService.add_bus(driver_id, data)
        return ResponseHandler.success("Bus added successfully", result)

    @jwt_required()
    def get(self):
        driver_id = get_jwt_identity()

        result = DriverService.get_driver_buses(driver_id)
        return ResponseHandler.success("Buses fetched successfully", result)


@driver_ns.route("/bus/<int:bus_id>/seats")
class BusSeats(Resource):
    @jwt_required()
    def get(self, bus_id):
        driver_id = get_jwt_identity()

        result = DriverService.get_bus_seats(driver_id, bus_id)
        if 'error' in result:
            return ResponseHandler.error(result['error'], 404)
        return ResponseHandler.success("Bus seats fetched successfully", result)


@driver_ns.route("/bus/<int:bus_id>/assign_route")
class AssignRoute(Resource):
    @jwt_required()
    def put(self, bus_id):
        data = request.get_json()
        driver_id = get_jwt_identity()

        route_id = data.get('route_id')
        if not route_id:
            return ResponseHandler.error("route_id is required", 400)

        result = DriverService.assign_bus_to_route(driver_id, bus_id, route_id)
        if 'error' in result:
            return ResponseHandler.error(result['error'], 404)
        return ResponseHandler.success("Bus assigned to route successfully")


@driver_ns.route("/bus/<int:bus_id>/set_departure_time")
class SetDepartureTime(Resource):
    @jwt_required()
    def put(self, bus_id):
        data = request.get_json()
        driver_id = get_jwt_identity()

        result = DriverService.set_departure_time(driver_id, bus_id, data)
        if 'error' in result:
            return ResponseHandler.error(result['error'], 404)
        return ResponseHandler.success("Departure time set successfully")


@driver_ns.route("/bus/<int:bus_id>/set_ticket_price")
class SetTicketPrice(Resource):
    @jwt_required()
    def put(self, bus_id):
        data = request.get_json()
        driver_id = get_jwt_identity()

        result = DriverService.set_ticket_price(driver_id, bus_id, data)
        if 'error' in result:
            return ResponseHandler.error(result['error'], 404)
        return ResponseHandler.success("Ticket price updated successfully")


@driver_ns.route("/bus/<int:bus_id>")
class DeleteBus(Resource):
    @jwt_required()
    def delete(self, bus_id):
        driver_id = get_jwt_identity()

        result = DriverService.delete_bus(driver_id, bus_id)
        if 'error' in result:
            return ResponseHandler.error(result['error'], 404)
        return ResponseHandler.success("Bus deleted successfully")

from flask_restx import Namespace, Resource
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.driver_service import DriverService

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
        return jsonify(result)


@driver_ns.route("/buses")
class DriverBuses(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        driver_id = get_jwt_identity()

        result = DriverService.add_bus(driver_id, data)
        return jsonify(result)

    @jwt_required()
    def get(self):
        driver_id = get_jwt_identity()

        result = DriverService.get_driver_buses(driver_id)
        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>/seats")
class BusSeats(Resource):
    @jwt_required()
    def get(self, bus_id):
        driver_id = get_jwt_identity()

        result = DriverService.get_bus_seats(driver_id, bus_id)
        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>/assign_route")
class AssignRoute(Resource):
    @jwt_required()
    def put(self, bus_id):
        data = request.get_json()
        driver_id = get_jwt_identity()

        result = DriverService.assign_bus_to_route(driver_id, bus_id, data)
        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>/set_departure_time")
class SetDepartureTime(Resource):
    @jwt_required()
    def put(self, bus_id):
        data = request.get_json()
        driver_id = get_jwt_identity()

        result = DriverService.set_departure_time(driver_id, bus_id, data)
        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>/set_ticket_price")
class SetTicketPrice(Resource):
    @jwt_required()
    def put(self, bus_id):
        data = request.get_json()
        driver_id = get_jwt_identity()

        # This expects 'ticket_price', make sure the frontend sends that
        result = DriverService.set_ticket_price(driver_id, bus_id, data)
        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>")
class DeleteBus(Resource):
    @jwt_required()
    def delete(self, bus_id):
        driver_id = get_jwt_identity()

        result = DriverService.delete_bus(driver_id, bus_id)
        return jsonify(result)

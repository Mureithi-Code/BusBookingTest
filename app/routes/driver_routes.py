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
        current_app.logger.info(f'📦 Received data: {data}')
        driver_id = get_jwt_identity()
        current_app.logger.info(f'👤 Driver ID from token: {driver_id}')

        response, status = DriverService.create_route(driver_id, data)
        current_app.logger.info(f'✅ Response from service: {response} (Status: {status})')

        return response, status

    @jwt_required()
    def get(self):
        current_app.logger.info('🟡 [DRIVER ROUTE] GET /driver/routes called.')
        driver_id = get_jwt_identity()
        current_app.logger.info(f'👤 Driver ID from token: {driver_id}')

        result = DriverService.get_driver_routes(driver_id)
        current_app.logger.info(f'📊 Retrieved routes for driver {driver_id}: {result}')

        return jsonify(result)


@driver_ns.route("/routes/<int:driver_id>")
class SpecificDriverRoutes(Resource):
    def get(self, driver_id):
        current_app.logger.info(f'🟡 [DRIVER ROUTE] GET /driver/routes/{driver_id} called.')

        result = DriverService.get_driver_routes(driver_id)
        current_app.logger.info(f'📊 Retrieved routes for specific driver {driver_id}: {result}')

        return jsonify(result)


@driver_ns.route("/buses")
class DriverBuses(Resource):
    @jwt_required()
    def post(self):
        current_app.logger.info('🟡 [DRIVER BUS] POST /driver/buses called.')
        data = request.get_json()
        current_app.logger.info(f'📦 Received data: {data}')
        driver_id = get_jwt_identity()
        current_app.logger.info(f'👤 Driver ID from token: {driver_id}')

        result = DriverService.add_bus(driver_id, data)
        current_app.logger.info(f'✅ Bus added for driver {driver_id}. Result: {result}')

        return jsonify(result)

    @jwt_required()
    def get(self):
        current_app.logger.info('🟡 [DRIVER BUS] GET /driver/buses called.')
        driver_id = get_jwt_identity()
        current_app.logger.info(f'👤 Driver ID from token: {driver_id}')

        result = DriverService.get_driver_buses(driver_id)
        current_app.logger.info(f'📊 Retrieved buses for driver {driver_id}: {result}')

        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>/seats")
class BusSeats(Resource):
    @jwt_required()
    def get(self, bus_id):
        current_app.logger.info(f'🟡 [BUS SEATS] GET /driver/bus/{bus_id}/seats called.')
        driver_id = get_jwt_identity()
        current_app.logger.info(f'👤 Driver ID from token: {driver_id}')

        result = DriverService.get_bus_seats(driver_id, bus_id)
        current_app.logger.info(f'📊 Retrieved seats for bus {bus_id}: {result}')

        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>/assign_route")
class AssignRoute(Resource):
    @jwt_required()
    def put(self, bus_id):
        current_app.logger.info(f'🟡 [ASSIGN ROUTE] PUT /driver/bus/{bus_id}/assign_route called.')
        data = request.get_json()
        current_app.logger.info(f'📦 Received data: {data}')
        driver_id = get_jwt_identity()
        current_app.logger.info(f'👤 Driver ID from token: {driver_id}')

        result = DriverService.assign_bus_to_route(driver_id, bus_id, data)
        current_app.logger.info(f'✅ Bus {bus_id} assigned to route. Result: {result}')

        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>/set_departure_time")
class SetDepartureTime(Resource):
    @jwt_required()
    def put(self, bus_id):
        current_app.logger.info(f'🟡 [SET DEPARTURE TIME] PUT /driver/bus/{bus_id}/set_departure_time called.')
        data = request.get_json()
        current_app.logger.info(f'📦 Received data: {data}')
        driver_id = get_jwt_identity()
        current_app.logger.info(f'👤 Driver ID from token: {driver_id}')

        result = DriverService.set_departure_time(driver_id, bus_id, data)
        current_app.logger.info(f'✅ Departure time set for bus {bus_id}. Result: {result}')

        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>/set_ticket_price")
class SetTicketPrice(Resource):
    @jwt_required()
    def put(self, bus_id):
        current_app.logger.info(f'🟡 [SET TICKET PRICE] PUT /driver/bus/{bus_id}/set_ticket_price called.')
        data = request.get_json()
        current_app.logger.info(f'📦 Received data: {data}')
        driver_id = get_jwt_identity()
        current_app.logger.info(f'👤 Driver ID from token: {driver_id}')

        result = DriverService.set_ticket_price(driver_id, bus_id, data)
        current_app.logger.info(f'✅ Ticket price set for bus {bus_id}. Result: {result}')

        return jsonify(result)


@driver_ns.route("/bus/<int:bus_id>")
class DeleteBus(Resource):
    @jwt_required()
    def delete(self, bus_id):
        current_app.logger.info(f'🟡 [DELETE BUS] DELETE /driver/bus/{bus_id} called.')
        driver_id = get_jwt_identity()
        current_app.logger.info(f'👤 Driver ID from token: {driver_id}')

        result = DriverService.delete_bus(driver_id, bus_id)
        current_app.logger.info(f'✅ Bus {bus_id} deleted. Result: {result}')

        return jsonify(result)

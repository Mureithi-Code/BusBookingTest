from flask import current_app
from app.extensions import db
from app.models.bus import Bus
from app.models.route import Route
from app.models.booking import Booking
from app.utils.response import ResponseHandler

class DriverService:

    @staticmethod
    def create_route(driver_id, data):
        current_app.logger.info(f'🚍 Creating new route for Driver ID: {driver_id}')
        try:
            new_route = Route(
                start_location=data['start_location'],
                destination=data['destination'],
                driver_id=driver_id
            )
            db.session.add(new_route)
            db.session.commit()

            current_app.logger.info(f'✅ Route created successfully for Driver ID: {driver_id}')
            return ResponseHandler.success("Route created successfully", {"route_id": new_route.id})
        except Exception as e:
            current_app.logger.error(f'❌ Error creating route: {str(e)}')
            db.session.rollback()
            return ResponseHandler.error("Failed to create route", 500)

    @staticmethod
    def get_driver_routes(driver_id):
        try:
            routes = Route.query.filter_by(driver_id=driver_id).all()
            route_list = [
                {
                    "id": route.id,
                    "start_location": route.start_location,
                    "destination": route.destination,
                    "departure_time": route.departure_time
                }
                for route in routes
            ]
            return {"success": True, "routes": route_list}
        except Exception as e:
            current_app.logger.error(f"❌ Error fetching routes for driver {driver_id}: {str(e)}")
            return ResponseHandler.error("Failed to fetch routes", 500)

    @staticmethod
    def add_bus(driver_id, data):
        try:
            new_bus = Bus(
                driver_id=driver_id,
                bus_number=data['bus_number'],
                capacity=data['capacity'],
                available_seats=data['capacity'],
                ticket_price=data.get('ticket_price', 0),
                route_id=None
            )
            db.session.add(new_bus)
            db.session.commit()

            return ResponseHandler.success("Bus added successfully", {"bus_id": new_bus.id})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error adding bus: {str(e)}')
            return ResponseHandler.error("Failed to add bus", 500)

    @staticmethod
    def get_driver_buses(driver_id):
        try:
            buses = Bus.query.filter_by(driver_id=driver_id).all()
            bus_list = []
            for bus in buses:
                route = bus.route
                bus_list.append({
                    "id": bus.id,
                    "bus_number": bus.bus_number,
                    "capacity": bus.capacity,
                    "available_seats": bus.available_seats,
                    "route_id": bus.route_id,
                    "start_location": route.start_location if route else None,
                    "destination": route.destination if route else None,
                    "departure_time": route.departure_time if route else None,
                    "ticket_price": bus.ticket_price
                })
            return {"success": True, "buses": bus_list}
        except Exception as e:
            current_app.logger.error(f"❌ Error fetching buses for driver {driver_id}: {str(e)}")
            return ResponseHandler.error("Failed to fetch buses", 500)

    @staticmethod
    def assign_bus_to_route(driver_id, bus_id, route_id):
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return {"success": False, "message": "Bus not found or you don't own this bus"}, 404

        route = Route.query.filter_by(id=route_id, driver_id=driver_id).first()
        if not route:
            return {"success": False, "message": "Route not found or you don't own this route"}, 404

        try:
            bus.route_id = route.id
            db.session.commit()
            return ResponseHandler.success("Bus assigned to route successfully")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error assigning bus to route: {str(e)}')
            return ResponseHandler.error("Failed to assign bus to route", 500)

    @staticmethod
    def set_departure_time(driver_id, bus_id, data):
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return {"success": False, "message": "Bus not found or you don't own this bus"}, 404

        if not bus.route:
            return {"success": False, "message": "This bus has no assigned route"}, 400

        try:
            bus.route.departure_time = data['departure_time']
            db.session.commit()
            return ResponseHandler.success("Departure time set successfully")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error setting departure time: {str(e)}')
            return ResponseHandler.error("Failed to set departure time", 500)

    @staticmethod
    def set_ticket_price(driver_id, bus_id, data):
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return {"success": False, "message": "Bus not found or you don't own this bus"}, 404

        try:
            bus.ticket_price = data['ticket_price']
            db.session.commit()
            return ResponseHandler.success("Ticket price updated successfully")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error updating ticket price: {str(e)}')
            return ResponseHandler.error("Failed to update ticket price", 500)

    @staticmethod
    def delete_bus(driver_id, bus_id):
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return {"success": False, "message": "Bus not found or you don't own this bus"}, 404

        try:
            db.session.delete(bus)
            db.session.commit()
            return ResponseHandler.success("Bus deleted successfully")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error deleting bus: {str(e)}')
            return ResponseHandler.error("Failed to delete bus", 500)

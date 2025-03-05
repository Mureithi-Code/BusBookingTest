from flask import current_app
from app.extensions import db
from app.models.bus import Bus
from app.models.route import Route
from app.models.booking import Booking
from app.utils.response import ResponseHandler
from app.serializers.serializer import serialize_route, serialize_bus

class DriverService:

    @staticmethod
    def create_route(driver_id, data):
        try:
            new_route = Route(
                start_location=data['start_location'],
                destination=data['destination'],
                driver_id=driver_id
            )
            db.session.add(new_route)
            db.session.commit()

            return ResponseHandler.success("Route created successfully", {"route_id": new_route.id})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error creating route: {str(e)}')
            return ResponseHandler.error("Failed to create route", 500)

    @staticmethod
    def get_driver_routes(driver_id):
        try:
            routes = Route.query.filter_by(driver_id=driver_id).all()
            route_list = [serialize_route(route) for route in routes]
            return ResponseHandler.success("Routes fetched successfully", {"routes": route_list})
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
            bus_list = [serialize_bus(bus) for bus in buses]
            return ResponseHandler.success("Buses fetched successfully", {"buses": bus_list})
        except Exception as e:
            current_app.logger.error(f"❌ Error fetching buses for driver {driver_id}: {str(e)}")
            return ResponseHandler.error("Failed to fetch buses", 500)

    @staticmethod
    def get_bus_seats(driver_id, bus_id):
        """
        Fetch all seats for a bus, showing which are booked and which are available.
        """
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return ResponseHandler.error("Bus not found or you don't own this bus", 404)

        # Fetch all booked seat numbers
        bookings = Booking.query.filter_by(bus_id=bus_id).all()
        booked_seats = {booking.seat_number for booking in bookings}

        # Create seat list with individual seat status (booked/available)
        all_seats = [
            serialize_seat(seat_number, seat_number in booked_seats)
            for seat_number in range(1, bus.capacity + 1)
        ]

        data = {
            "bus_id": bus.id,
            "bus_number": bus.bus_number,
            "total_seats": bus.capacity,
            "available_seats": bus.available_seats,
            "seats": all_seats  # Full seat breakdown with status
        }

        return ResponseHandler.success("Bus seats fetched successfully", data)

    @staticmethod
    def assign_bus_to_route(driver_id, bus_id, route_id):
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return ResponseHandler.error("Bus not found or you don't own this bus", 404)

        route = Route.query.filter_by(id=route_id, driver_id=driver_id).first()
        if not route:
            return ResponseHandler.error("Route not found or you don't own this route", 404)

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
            return ResponseHandler.error("Bus not found or you don't own this bus", 404)

        if not bus.route:
            return ResponseHandler.error("This bus has no assigned route", 400)

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
            return ResponseHandler.error("Bus not found or you don't own this bus", 404)

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
            return ResponseHandler.error("Bus not found or you don't own this bus", 404)

        try:
            db.session.delete(bus)
            db.session.commit()
            return ResponseHandler.success("Bus deleted successfully")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error deleting bus: {str(e)}')
            return ResponseHandler.error("Failed to delete bus", 500)

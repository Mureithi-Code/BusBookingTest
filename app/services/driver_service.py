from flask import current_app
from app.extensions import db
from app.models.bus import Bus
from app.models.route import Route
from app.models.booking import Booking

class DriverService:

    @staticmethod
    def create_route(driver_id, data):
        """Create a new route for the logged-in driver"""
        current_app.logger.info(f'🚍 Creating new route for Driver ID: {driver_id}')
        current_app.logger.info(f'📦 Route Data: {data}')

        new_route = Route(
            start_location=data['start_location'],
            destination=data['destination'],
            driver_id=driver_id
        )
        db.session.add(new_route)
        try:
            db.session.commit()
            current_app.logger.info(f'✅ Route created successfully for Driver ID: {driver_id}')
            return {"message": "Route created successfully"}, 201
        except Exception as e:
            current_app.logger.error(f'❌ Error creating route: {str(e)}')
            db.session.rollback()
            return {"error": "Failed to create route"}, 500

    @staticmethod
    def get_driver_routes(driver_id):
        """Get all routes created by this driver"""
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
        return {"routes": route_list}

    @staticmethod
    def add_bus(driver_id, data):
        """Add a new bus for this driver"""
        new_bus = Bus(
            driver_id=driver_id,
            bus_number=data['bus_number'],
            capacity=data['capacity'],
            available_seats=data['capacity'],
            ticket_price=data.get('ticket_price', 0),
            route_id=None
        )
        db.session.add(new_bus)
        try:
            db.session.commit()
            return {"message": "Bus added successfully", "bus_id": new_bus.id}, 201
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error adding bus: {str(e)}')
            return {"error": "Failed to add bus"}, 500

    @staticmethod
    def get_driver_buses(driver_id):
        """Get all buses owned by this driver"""
        try:
            buses = Bus.query.filter_by(driver_id=driver_id).all()
            bus_list = []
            for bus in buses:
                route = bus.route  # assuming bus has a backref `route`
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
            current_app.logger.error(f"Failed to fetch buses for driver {driver_id}: {str(e)}")
            return {"success": False, "error": "Failed to fetch buses"}, 500

    @staticmethod
    def get_bus_seats(driver_id, bus_id):
        """Get available and booked seats for a specific bus"""
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return {"error": "Bus not found or you don't own this bus"}, 404

        booked_seats = Booking.query.filter_by(bus_id=bus_id).count()

        return {
            "bus_id": bus.id,
            "bus_number": bus.bus_number,
            "total_seats": bus.capacity,
            "available_seats": bus.available_seats,
            "booked_seats": booked_seats
        }

    @staticmethod
    def assign_bus_to_route(driver_id, bus_id, route_id):
        """Assign a bus to a route"""
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return {"error": "Bus not found or you don't own this bus"}, 404

        route = Route.query.filter_by(id=route_id, driver_id=driver_id).first()
        if not route:
            return {"error": "Route not found or you don't own this route"}, 404

        bus.route_id = route.id
        try:
            db.session.commit()
            return {"message": "Bus assigned to route successfully"}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error assigning bus to route: {str(e)}')
            return {"error": "Failed to assign bus to route"}, 500

    @staticmethod
    def set_departure_time(driver_id, bus_id, data):
        """Set the departure time for a bus's route"""
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return {"error": "Bus not found or you don't own this bus"}, 404

        if not bus.route:
            return {"error": "This bus has no assigned route"}, 400

        bus.route.departure_time = data['departure_time']
        try:
            db.session.commit()
            return {"message": "Departure time set successfully"}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error setting departure time: {str(e)}')
            return {"error": "Failed to set departure time"}, 500

    @staticmethod
    def set_ticket_price(driver_id, bus_id, data):
        """Set or update ticket price per seat for a bus"""
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return {"error": "Bus not found or you don't own this bus"}, 404

        bus.ticket_price = data['ticket_price']
        try:
            db.session.commit()
            return {"message": "Ticket price updated successfully"}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error updating ticket price: {str(e)}')
            return {"error": "Failed to update ticket price"}, 500

    @staticmethod
    def delete_bus(driver_id, bus_id):
        """Delete a bus if owned by the driver"""
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            return {"error": "Bus not found or you don't own this bus"}, 404

        try:
            db.session.delete(bus)
            db.session.commit()
            return {"message": "Bus deleted successfully"}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ Error deleting bus: {str(e)}')
            return {"error": "Failed to delete bus"}, 500

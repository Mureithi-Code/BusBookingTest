from app.extensions import db
from app.models.user import User
from app.models.bus import Bus
from app.models.route import Route
from app.models.message import Message
from app.utils.response import ResponseHandler
from app.serializers.serializer import serialize_bus, serialize_route, serialize_message, serialize_driver

class AdminService:

    @staticmethod
    def get_all_buses():
        try:
            buses = Bus.query.all()
            bus_list = [serialize_bus(bus) for bus in buses]
            return ResponseHandler.success("All buses fetched successfully", bus_list)
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch buses: {str(e)}", 500)

    @staticmethod
    def get_all_routes():
        try:
            routes = Route.query.all()
            route_list = [serialize_route(route) for route in routes]
            return ResponseHandler.success("All routes fetched successfully", route_list)
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch routes: {str(e)}", 500)

    @staticmethod
    def get_all_drivers():
        try:
            drivers = User.query.filter_by(role='Driver').all()
            driver_list = [serialize_driver(driver) for driver in drivers]
            return ResponseHandler.success("All drivers fetched successfully", driver_list)
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch drivers: {str(e)}", 500)

    @staticmethod
    def remove_driver(driver_id):
        try:
            driver = User.query.filter_by(id=driver_id, role='Driver').first()
            if not driver:
                return ResponseHandler.error("Driver not found", 404)

            # Optional: Check if driver has assigned buses/routes and handle cleanup
            Bus.query.filter_by(driver_id=driver_id).update({"driver_id": None})
            Route.query.filter_by(driver_id=driver_id).update({"driver_id": None})

            db.session.delete(driver)
            db.session.commit()

            return ResponseHandler.success("Driver removed successfully")
        except Exception as e:
            db.session.rollback()
            return ResponseHandler.error(f"Failed to remove driver: {str(e)}", 500)

    @staticmethod
    def cancel_route(route_id):
        try:
            route = Route.query.get(route_id)
            if not route:
                return ResponseHandler.error("Route not found", 404)

            # Optionally unassign the bus if needed
            if route.bus_id:
                bus = Bus.query.get(route.bus_id)
                if bus:
                    bus.route_id = None

            db.session.delete(route)
            db.session.commit()

            return ResponseHandler.success("Route canceled successfully")
        except Exception as e:
            db.session.rollback()
            return ResponseHandler.error(f"Failed to cancel route: {str(e)}", 500)

    @staticmethod
    def get_all_messages():
        try:
            messages = Message.query.all()
            message_list = [serialize_message(message) for message in messages]
            return ResponseHandler.success("All messages fetched successfully", message_list)
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch messages: {str(e)}", 500)

    @staticmethod
    def reply_to_message(message_id, data):
        try:
            original_message = Message.query.get(message_id)
            if not original_message:
                return ResponseHandler.error("Message not found", 404)

            reply = Message(
                sender_id=data['sender_id'],  # Admin's ID
                receiver_id=original_message.sender_id,  # Reply to original sender (customer)
                content=data['content']
            )

            db.session.add(reply)
            db.session.commit()

            return ResponseHandler.success("Reply sent successfully")
        except Exception as e:
            db.session.rollback()
            return ResponseHandler.error(f"Failed to send reply: {str(e)}", 500)


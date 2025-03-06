from app.extensions import db
from app.models.bus import Bus
from app.models.route import Route
from app.models.driver import Driver
from app.models.message import Message
from app.utils.response import ResponseHandler
from app.serializers.serializer import serialize_bus, serialize_route, serialize_message, serialize_driver

class AdminService:

    @staticmethod
    def get_all_buses():
        try:
            buses = Bus.query.all()
            bus_list = [serialize_bus(bus) for bus in buses]
            return ResponseHandler.success("All buses fetched successfully", {"buses": bus_list})
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch buses: {str(e)}", 500)

    @staticmethod
    def get_all_routes():
        try:
            routes = Route.query.all()
            route_list = [serialize_route(route) for route in routes]
            return ResponseHandler.success("All routes fetched successfully", {"routes": route_list})
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch routes: {str(e)}", 500)

    @staticmethod
    def get_all_drivers():
        try:
            drivers = Driver.query.all()
            driver_list = [serialize_driver(driver) for driver in drivers]
            return ResponseHandler.success("All drivers fetched successfully", {"drivers": driver_list})
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch drivers: {str(e)}", 500)

    @staticmethod
    def remove_driver(driver_id):
        driver = Driver.query.get(driver_id)
        if not driver:
            return ResponseHandler.error("Driver not found", 404)

        try:
            db.session.delete(driver)
            db.session.commit()
            return ResponseHandler.success("Driver removed successfully")
        except Exception as e:
            db.session.rollback()
            return ResponseHandler.error(f"Failed to remove driver: {str(e)}", 500)

    @staticmethod
    def cancel_route(route_id):
        route = Route.query.get(route_id)
        if not route:
            return ResponseHandler.error("Route not found", 404)

        try:
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
            return ResponseHandler.success("All messages fetched successfully", {"messages": message_list})
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch messages: {str(e)}", 500)

    @staticmethod
    def reply_to_message(message_id, data):
        message = Message.query.get(message_id)
        if not message:
            return ResponseHandler.error("Message not found", 404)

        try:
            reply_message = Message(
                sender_id=1,  # Assuming admin is user ID 1
                receiver_id=message.sender_id,
                content=data.get('content')
            )
            db.session.add(reply_message)
            db.session.commit()

            return ResponseHandler.success("Reply sent successfully")
        except Exception as e:
            db.session.rollback()
            return ResponseHandler.error(f"Failed to send reply: {str(e)}", 500)

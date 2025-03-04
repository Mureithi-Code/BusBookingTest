from flask_restx import Namespace, Resource
from flask import request
from app.services.customer_service import CustomerService

# Define Namespace for Swagger documentation
customer_ns = Namespace("Customer", description="Customer Booking & Messaging Endpoints")

@customer_ns.route("/routes")
class GetAllRoutes(Resource):
    def get(self):
        """Get all available routes"""
        return CustomerService.get_all_routes()

@customer_ns.route("/buses")
class GetAllBuses(Resource):
    def get(self):
        """Get all available buses"""
        return CustomerService.get_all_buses()

@customer_ns.route("/view_available_seats/<int:bus_id>")
class ViewAvailableSeats(Resource):
    def get(self, bus_id):
        """View available and booked seats for a specific bus"""
        return CustomerService.view_available_seats(bus_id)

@customer_ns.route("/book_seat")
class BookSeat(Resource):
    def post(self):
        """Book a seat on a selected bus"""
        data = request.get_json()
        return CustomerService.book_seat(data)

@customer_ns.route("/cancel_booking/<int:booking_id>")
class CancelBooking(Resource):
    def delete(self, booking_id):
        """Cancel a booking by booking ID"""
        return CustomerService.cancel_booking(booking_id)

@customer_ns.route("/edit_booking/<int:booking_id>")
class EditBooking(Resource):
    def put(self, booking_id):
        """Edit a booking to change bus or seat number"""
        data = request.get_json()
        return CustomerService.edit_booking(booking_id, data)

@customer_ns.route("/send_message")
class SendMessage(Resource):
    def post(self):
        """Send a message to the admin"""
        data = request.get_json()
        return CustomerService.send_message_to_admin(data)

@customer_ns.route("/reply_to_message/<int:message_id>")
class ReplyToMessage(Resource):
    def post(self, message_id):
        """Reply to an admin message by message ID"""
        data = request.get_json()
        return CustomerService.reply_to_admin_message(message_id, data)

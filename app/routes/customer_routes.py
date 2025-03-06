from flask_restx import Namespace, Resource
from flask import request, current_app
from app.services.customer_service import CustomerService

# Define Namespace for Swagger documentation
customer_ns = Namespace("Customer", description="Customer Booking & Messaging Endpoints")

@customer_ns.route("/routes")
class GetAllRoutes(Resource):
    def get(self):
        """Get all available routes"""
        current_app.logger.info("📥 [CUSTOMER] GET /customer/routes")
        response, status = CustomerService.get_all_routes()
        return response, status


@customer_ns.route("/buses")
class GetAllBuses(Resource):
    def get(self):
        """Get all available buses"""
        current_app.logger.info("📥 [CUSTOMER] GET /customer/buses")
        response, status = CustomerService.get_all_buses()
        return response, status


@customer_ns.route("/view_available_seats/<int:bus_id>")
class ViewAvailableSeats(Resource):
    def get(self, bus_id):
        """View available and booked seats for a specific bus"""
        current_app.logger.info(f"📥 [CUSTOMER] GET /customer/view_available_seats/{bus_id}")
        response, status = CustomerService.view_available_seats(bus_id)
        return response, status


@customer_ns.route("/book_seat")
class BookSeat(Resource):
    def post(self):
        """Book a seat on a selected bus"""
        current_app.logger.info("📥 [CUSTOMER] POST /customer/book_seat")
        data = request.get_json()
        response, status = CustomerService.book_seat(data)
        return response, status


@customer_ns.route("/cancel_booking/<int:booking_id>")
class CancelBooking(Resource):
    def delete(self, booking_id):
        """Cancel a booking by booking ID"""
        current_app.logger.info(f"📥 [CUSTOMER] DELETE /customer/cancel_booking/{booking_id}")
        response, status = CustomerService.cancel_booking(booking_id)
        return response, status


@customer_ns.route("/edit_booking/<int:booking_id>")
class EditBooking(Resource):
    def put(self, booking_id):
        """Edit a booking to change bus or seat number"""
        current_app.logger.info(f"📥 [CUSTOMER] PUT /customer/edit_booking/{booking_id}")
        data = request.get_json()
        response, status = CustomerService.edit_booking(booking_id, data)
        return response, status


@customer_ns.route("/send_message")
class SendMessage(Resource):
    def post(self):
        """Send a message to the admin"""
        current_app.logger.info("📥 [CUSTOMER] POST /customer/send_message")
        data = request.get_json()
        response, status = CustomerService.send_message_to_admin(data)
        return response, status


@customer_ns.route("/reply_to_message/<int:message_id>")
class ReplyToMessage(Resource):
    def post(self, message_id):
        """Reply to an admin message by message ID"""
        current_app.logger.info(f"📥 [CUSTOMER] POST /customer/reply_to_message/{message_id}")
        data = request.get_json()
        response, status = CustomerService.reply_to_admin_message(message_id, data)
        return response, status

@customer_ns.route("/my_bookings/<int:customer_id>")
class GetMyBookings(Resource):
    def get(self, customer_id):
        """Get all bookings for a specific customer"""
        current_app.logger.info(f"📥 [CUSTOMER] GET /customer/my_bookings/{customer_id}")
        response, status = CustomerService.get_my_bookings(customer_id)
        current_app.logger.info(f"✅ Bookings Response: {response}")
        return response, status

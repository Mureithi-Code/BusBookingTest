from flask_restx import Namespace, Resource
from flask import request
from app.services.customer_service import CustomerService

# Define Namespace for Swagger documentation
customer_ns = Namespace("Customer", description="Customer Booking & Messaging Endpoints")

@customer_ns.route("/book_seat")
class BookSeat(Resource):
    def post(self):
        """Book a seat on an available bus"""
        data = request.get_json()
        return CustomerService.book_seat(data)

@customer_ns.route("/cancel_booking/<int:booking_id>")
class CancelBooking(Resource):
    def delete(self, booking_id):
        """Cancel a booking by booking ID"""
        return CustomerService.cancel_booking(booking_id)

@customer_ns.route("/view_available_seats/<int:bus_id>")
class ViewAvailableSeats(Resource):
    def get(self, bus_id):
        """View available seats for a given bus"""
        return CustomerService.view_available_seats(bus_id)

@customer_ns.route("/send_message")
class SendMessage(Resource):
    def post(self):
        """Send a message to the admin"""
        data = request.get_json()
        return CustomerService.send_message(data)

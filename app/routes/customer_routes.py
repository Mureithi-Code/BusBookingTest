from flask import Blueprint, request
from app.services.customer_service import CustomerService

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/book_seat', methods=['POST'])
def book_seat():
    data = request.get_json()
    return CustomerService.book_seat(data)

@customer_bp.route('/cancel_booking/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    return CustomerService.cancel_booking(booking_id)

@customer_bp.route('/view_available_seats/<int:bus_id>', methods=['GET'])
def view_available_seats(bus_id):
    return CustomerService.view_available_seats(bus_id)

@customer_bp.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    return CustomerService.send_message(data)

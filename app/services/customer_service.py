from app.extensions import db
from app.models.booking import Booking
from app.models.bus import Bus
from flask import jsonify

class CustomerService:
    @staticmethod
    def book_seat(data):
        bus = Bus.query.get(data['bus_id'])
        if not bus or bus.available_seats == 0:
            return jsonify({"error": "No available seats"}), 400
        
        booking = Booking(customer_id=data['customer_id'], bus_id=data['bus_id'], seat_number=data['seat_number'])
        bus.available_seats -= 1
        db.session.add(booking)
        db.session.commit()
        return jsonify({"message": "Seat booked successfully"}), 201

    @staticmethod
    def cancel_booking(booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"error": "Booking not found"}), 404
        
        bus = Bus.query.get(booking.bus_id)
        bus.available_seats += 1
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Booking canceled successfully"}), 200

    @staticmethod
    def view_available_seats(bus_id):
        bus = Bus.query.get(bus_id)
        if not bus:
            return jsonify({"error": "Bus not found"}), 404
        return jsonify({"available_seats": bus.available_seats}), 200

from app.extensions import db
from app.models.booking import Booking
from app.models.bus import Bus
from app.models.route import Route
from app.models.message import Message  # Assuming this model exists
from flask import jsonify

class CustomerService:

    @staticmethod
    def get_all_routes():
        routes = Route.query.all()
        route_list = [
            {
                "id": route.id,
                "start_location": route.start_location,
                "destination": route.destination,
                "departure_time": route.departure_time,
                "driver_id": route.driver_id
            }
            for route in routes
        ]
        return jsonify({"routes": route_list}), 200

    @staticmethod
    def get_all_buses():
        buses = Bus.query.all()
        bus_list = [
            {
                "id": bus.id,
                "route_id": bus.route_id,
                "bus_number": bus.bus_number,
                "capacity": bus.capacity,
                "available_seats": bus.available_seats,
                "ticket_price": bus.ticket_price
            }
            for bus in buses
        ]
        return jsonify({"buses": bus_list}), 200

    @staticmethod
    def view_all_seats(bus_id):
        bus = Bus.query.get(bus_id)
        if not bus:
            return jsonify({"error": "Bus not found"}), 404

        # Get all bookings for this bus
        bookings = Booking.query.filter_by(bus_id=bus_id).all()
        booked_seats = [booking.seat_number for booking in bookings]

        all_seats = [
            {"seat_number": seat_number, "status": "booked" if seat_number in booked_seats else "available"}
            for seat_number in range(1, bus.capacity + 1)
        ]

        return jsonify({
            "bus_id": bus_id,
            "bus_number": bus.bus_number,
            "seats": all_seats
        }), 200

    @staticmethod
    def book_seat(data):
        bus = Bus.query.get(data['bus_id'])
        if not bus:
            return jsonify({"error": "Bus not found"}), 404

        if bus.available_seats <= 0:
            return jsonify({"error": "No available seats"}), 400

        # Check if seat is already booked
        existing_booking = Booking.query.filter_by(
            bus_id=data['bus_id'], seat_number=data['seat_number']
        ).first()

        if existing_booking:
            return jsonify({"error": "Seat already booked"}), 400

        # Create new booking
        booking = Booking(
            customer_id=data['customer_id'],
            bus_id=data['bus_id'],
            route_id=bus.route_id,
            seat_number=data['seat_number']
        )
        bus.available_seats -= 1
        db.session.add(booking)
        db.session.commit()

        return jsonify({"message": "Seat booked successfully"}), 201

    @staticmethod
    def cancel_booking(booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        # Free up the seat
        bus = Bus.query.get(booking.bus_id)
        if bus:
            bus.available_seats += 1

        db.session.delete(booking)
        db.session.commit()

        return jsonify({"message": "Booking canceled successfully"}), 200

    @staticmethod
    def edit_booking(booking_id, data):
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        old_bus = Bus.query.get(booking.bus_id)
        new_bus = Bus.query.get(data['new_bus_id'])

        if not new_bus:
            return jsonify({"error": "New bus not found"}), 404

        # Check if seat is available on the new bus
        existing_booking = Booking.query.filter_by(
            bus_id=data['new_bus_id'], seat_number=data['new_seat_number']
        ).first()

        if existing_booking:
            return jsonify({"error": "Seat already booked"}), 400

        # Update booking
        booking.bus_id = data['new_bus_id']
        booking.seat_number = data['new_seat_number']
        booking.route_id = new_bus.route_id  # Update route if bus has a different route

        if old_bus:
            old_bus.available_seats += 1
        new_bus.available_seats -= 1

        db.session.commit()

        return jsonify({"message": "Booking updated successfully"}), 200

    @staticmethod
    def send_message_to_admin(data):
        message = Message(
            sender_id=data['customer_id'],
            receiver_id=data['admin_id'],  # Assuming admin ID is provided
            content=data['content']
        )
        db.session.add(message)
        db.session.commit()

        return jsonify({"message": "Message sent to admin"}), 201

    @staticmethod
    def reply_to_admin_message(message_id, data):
        message = Message.query.get(message_id)
        if not message:
            return jsonify({"error": "Message not found"}), 404

        reply = Message(
            sender_id=data['customer_id'],
            receiver_id=message.sender_id,  # Reply back to the admin who sent the original
            content=data['content']
        )
        db.session.add(reply)
        db.session.commit()

        return jsonify({"message": "Reply sent successfully"}), 201

    @staticmethod
    def view_available_seats(bus_id):
        # Use the same logic as view_all_seats for consistency
        return CustomerService.view_all_seats(bus_id)


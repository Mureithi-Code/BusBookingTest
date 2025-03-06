from flask import current_app
from app.extensions import db
from app.models.booking import Booking
from app.models.bus import Bus
from app.models.route import Route
from app.models.message import Message  
from app.utils.response import ResponseHandler
from app.serializers.serializer import serialize_route, serialize_bus, serialize_booking, serialize_seat

class CustomerService:

    @staticmethod
    def get_all_routes():
        try:
            routes = Route.query.all()
            route_list = [serialize_route(route) for route in routes]
            return ResponseHandler.success("Routes fetched successfully", route_list)
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch routes: {str(e)}", 500)

    @staticmethod
    def get_all_buses():
        try:
            buses = Bus.query.all()
            bus_list = [serialize_bus(bus) for bus in buses]
            return ResponseHandler.success("Buses fetched successfully", bus_list)
        except Exception as e:
            return ResponseHandler.error(f"Failed to fetch buses: {str(e)}", 500)

    @staticmethod
    def view_all_seats(bus_id):
        bus = Bus.query.get(bus_id)
        if not bus:
            return ResponseHandler.error("Bus not found", 404)

        bookings = Booking.query.filter_by(bus_id=bus_id).all()
        booked_seats = {booking.seat_number for booking in bookings}

        all_seats = [
            serialize_seat(seat_number, seat_number in booked_seats)
            for seat_number in range(1, bus.capacity + 1)
        ]

        return ResponseHandler.success(
            "Seats fetched successfully",
            {"bus_id": bus.id, "bus_number": bus.bus_number, "seats": all_seats}
        )

    @staticmethod
    def book_seat(data):
        try:
            current_app.logger.info(f"📌 Received booking request: {data}")

            # Validate incoming data
            required_fields = ["customer_id", "bus_id", "seat_number"]
            for field in required_fields:
                if field not in data:
                    current_app.logger.error(f"❌ Missing required field: {field}")
                    return ResponseHandler.error(f"Missing required field: {field}", 400)

            customer_id = data["customer_id"]
            bus_id = data["bus_id"]
            seat_number = data["seat_number"]

            current_app.logger.info(f"🔍 Verifying bus {bus_id}")

            # Fetch bus
            bus = Bus.query.get(bus_id)
            if not bus:
                current_app.logger.error(f"❌ Bus with ID {bus_id} not found.")
                return ResponseHandler.error("Bus not found", 404)

            # Ensure bus has valid available seats
            if bus.available_seats is None or bus.available_seats < 0:
                current_app.logger.error(f"❌ Bus {bus_id} has invalid available_seats count: {bus.available_seats}")
                return ResponseHandler.error("Bus has invalid seat count", 500)

            current_app.logger.info(f"✅ Bus {bus_id} found, available seats: {bus.available_seats}")

            # Check if the seat is already booked
            existing_booking = Booking.query.filter_by(bus_id=bus_id, seat_number=seat_number).first()
            if existing_booking:
                current_app.logger.warning(f"⚠️ Seat {seat_number} on Bus {bus_id} is already booked.")
                return ResponseHandler.error(f"Seat {seat_number} is already booked", 400)

            # Ensure seat number is within bus capacity
            if seat_number < 1 or seat_number > bus.capacity:
                current_app.logger.error(f"❌ Seat number {seat_number} is out of range for Bus {bus_id} (capacity: {bus.capacity})")
                return ResponseHandler.error(f"Invalid seat number {seat_number} for this bus", 400)

            current_app.logger.info(f"✅ Seat {seat_number} is available on bus {bus_id}")

            # Create and save booking
            booking = Booking(
                customer_id=customer_id,
                bus_id=bus_id,
                route_id=bus.route_id,
                seat_number=seat_number
            )
            db.session.add(booking)

            # Update available seats
            if bus.available_seats > 0:
                bus.available_seats -= 1
            else:
                current_app.logger.error(f"❌ Bus {bus_id} has no available seats left (current: {bus.available_seats})")
                return ResponseHandler.error("No available seats left on this bus", 400)

            db.session.commit()

            current_app.logger.info(f"✅ Seat {seat_number} successfully booked on Bus {bus_id} for Customer {customer_id}")

            return ResponseHandler.success("Seat booked successfully", serialize_booking(booking), 201)

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"❌ Exception during seat booking: {str(e)}", exc_info=True)
            return ResponseHandler.error(f"Failed to book seat: {str(e)}", 500)

    @staticmethod
    def cancel_booking(booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return ResponseHandler.error("Booking not found", 404)

        try:
            bus = Bus.query.get(booking.bus_id)
            if bus:
                bus.available_seats += 1

            db.session.delete(booking)
            db.session.commit()

            return ResponseHandler.success("Booking canceled successfully")
        except Exception as e:
            db.session.rollback()
            return ResponseHandler.error(f"Failed to cancel booking: {str(e)}", 500)

    @staticmethod
    def edit_booking(booking_id, data):
        booking = Booking.query.get(booking_id)
        if not booking:
            return ResponseHandler.error("Booking not found", 404)

        old_bus = Bus.query.get(booking.bus_id)
        new_bus = Bus.query.get(data['new_bus_id'])

        if not new_bus:
            return ResponseHandler.error("New bus not found", 404)

        existing_booking = Booking.query.filter_by(
            bus_id=data['new_bus_id'], seat_number=data['new_seat_number']
        ).first()

        if existing_booking:
            return ResponseHandler.error("Seat already booked", 400)

        try:
            booking.bus_id = data['new_bus_id']
            booking.seat_number = data['new_seat_number']
            booking.route_id = new_bus.route_id

            if old_bus:
                old_bus.available_seats += 1
            new_bus.available_seats -= 1

            db.session.commit()

            return ResponseHandler.success("Booking updated successfully", serialize_booking(booking))
        except Exception as e:
            db.session.rollback()
            return ResponseHandler.error(f"Failed to update booking: {str(e)}", 500)

    @staticmethod
    def send_message_to_admin(data):
        try:
            message = Message(
                sender_id=data['customer_id'],
                receiver_id=data['admin_id'],
                content=data['content']
            )
            db.session.add(message)
            db.session.commit()

            return ResponseHandler.success("Message sent to admin successfully")
        except Exception as e:
            db.session.rollback()
            return ResponseHandler.error(f"Failed to send message: {str(e)}", 500)

    @staticmethod
    def reply_to_admin_message(message_id, data):
        message = Message.query.get(message_id)
        if not message:
            return ResponseHandler.error("Message not found", 404)

        try:
            reply = Message(
                sender_id=data['customer_id'],
                receiver_id=message.sender_id,
                content=data['content']
            )
            db.session.add(reply)
            db.session.commit()

            return ResponseHandler.success("Reply sent successfully")
        except Exception as e:
            db.session.rollback()
            return ResponseHandler.error(f"Failed to send reply: {str(e)}", 500)

    @staticmethod
    def view_available_seats(bus_id):
        return CustomerService.view_all_seats(bus_id)
    
    @staticmethod
    def get_my_bookings(customer_id):
        bookings = Booking.query.filter_by(customer_id=customer_id).all()
        if not bookings:
            current_app.logger.warning(f"⚠️ No bookings found for customer {customer_id}")
            return ResponseHandler.error("No bookings found", 404)

        booking_list = [serialize_booking(booking) for booking in bookings]
        current_app.logger.info(f"✅ Retrieved {len(booking_list)} bookings for customer {customer_id}")
        return ResponseHandler.success("Bookings retrieved", booking_list)


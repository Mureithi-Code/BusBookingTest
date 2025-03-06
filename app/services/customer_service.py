from app.extensions import db
from app.models.booking import Booking
from app.models.bus import Bus
from app.models.route import Route
from app.models.message import Message  # Assuming this model exists
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
        if 'customer_id' not in data or not data['customer_id']:
            return ResponseHandler.error("Customer ID is required.", 400)
        
        bus = Bus.query.get(data['bus_id'])
        if not bus:
            return ResponseHandler.error("Bus not found", 404)
        
        if not bus.route_id:
            return ResponseHandler.error("This bus is not assigned to any route. You cannot book a seat.", 400)

        if bus.available_seats <= 0:
            return ResponseHandler.error("No available seats", 400)

        existing_booking = Booking.query.filter_by(
            bus_id=data['bus_id'], seat_number=data['seat_number']
        ).first()

        if existing_booking:
            return ResponseHandler.error("Seat already booked", 400)

        try:
            booking = Booking(
                customer_id=data['customer_id'],
                bus_id=data['bus_id'],
                route_id=bus.route_id,
                seat_number=data['seat_number']
            )
            bus.available_seats -= 1
            db.session.add(booking)
            db.session.commit()

            return ResponseHandler.success("Seat booked successfully", serialize_booking(booking), 201)
        except Exception as e:
            db.session.rollback()
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
            return ResponseHandler.error("No bookings found", 404)

        booking_list = [serialize_booking(booking) for booking in bookings]
        return ResponseHandler.success("Bookings retrieved", booking_list)


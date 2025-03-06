def serialize_route(route):
    return {
        "id": route.id,
        "start_location": route.start_location,
        "destination": route.destination,
        "departure_time": route.departure_time.isoformat() if route.departure_time else None,
        "driver_id": route.driver_id  # Include driver_id if relevant to customer views
    }

def serialize_bus(bus):
    route = bus.route  
    return {
        "id": bus.id,
        "bus_number": bus.bus_number,
        "capacity": bus.capacity,
        "available_seats": bus.available_seats,
        "ticket_price": bus.ticket_price,
        "route_id": bus.route_id,
        "start_location": route.start_location if route else None,
        "destination": route.destination if route else None,
        "departure_time": route.departure_time.isoformat() if route and route.departure_time else None
    }

def serialize_booking(booking):
    return {
        "id": booking.id,
        "seat_number": booking.seat_number,
        "status": booking.status if hasattr(booking, "status") else "booked",  # fallback for customer-side
        "bus_id": booking.bus_id,
        "customer_id": booking.customer_id,
        "created_at": booking.created_at.isoformat() if booking.created_at else None
    }

def serialize_seat(seat_number, is_booked):
    """
    Used for view_all_seats and view_available_seats.
    """
    return {
        "seat_number": seat_number,
        "status": "booked" if is_booked else "available"
    }

def serialize_message(message):
    """
    If you want to expose customer-to-admin messages.
    """
    return {
        "id": message.id,
        "sender_id": message.sender_id,
        "receiver_id": message.receiver_id,
        "content": message.content,
        "timestamp": message.timestamp.isoformat() if message.timestamp else None
    }

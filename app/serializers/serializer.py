
def serialize_route(route):
    return {
        "id": route.id,
        "start_location": route.start_location,
        "destination": route.destination,
        "departure_time": route.departure_time.isoformat() if route.departure_time else None
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
        "status": booking.status,
        "bus_id": booking.bus_id,
        "user_id": booking.user_id,
        "created_at": booking.created_at.isoformat() if booking.created_at else None
    }

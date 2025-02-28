from app.extensions import db
from app.models.bus import Bus
from flask import jsonify

class DriverService:
    @staticmethod
    def add_bus(data):
        new_bus = Bus(
            driver_id=data['driver_id'],
            bus_number=data['bus_number'],
            capacity=data['capacity'],
            available_seats=data['capacity'],
            ticket_price=data.get('ticket_price')
        )
        db.session.add(new_bus)
        db.session.commit()
        return {"message": "Bus added successfully"}, 201

    @staticmethod
    def pick_route(data):
        bus = Bus.query.get(data['bus_id'])
        if not bus:
            return {"error": "Bus not found"}, 404
        bus.route_id = data['route_id']
        db.session.commit()
        return {"message": "Route assigned successfully"}, 200

    @staticmethod
    def assign_cost(bus_id, data):
        bus = Bus.query.get(bus_id)
        if not bus:
            return {"error": "Bus not found"}, 404
        bus.ticket_price = data['cost']
        db.session.commit()
        return {"message": "Ticket price updated"}, 200

    @staticmethod
    def get_driver_buses(driver_id):
        buses = Bus.query.filter_by(driver_id=driver_id).all()
        return [{"id": bus.id, 
                 "bus_number": bus.bus_number, 
                 "capacity": bus.capacity, 
                 "available_seats": bus.available_seats, 
                 "ticket_price": bus.ticket_price,
                 "route_id": bus.route_id} for bus in buses], 200

    @staticmethod
    def update_bus(bus_id, data):
        bus = Bus.query.get(bus_id)
        if not bus:
            return {"error": "Bus not found"}, 404

        bus.bus_number = data.get('bus_number', bus.bus_number)
        bus.capacity = data.get('capacity', bus.capacity)
        bus.available_seats = data.get('available_seats', bus.available_seats)
        bus.ticket_price = data.get('ticket_price', bus.ticket_price)
        db.session.commit()

        return {"message": "Bus updated successfully"}, 200

    @staticmethod
    def remove_bus(bus_id):
        bus = Bus.query.get(bus_id)
        if not bus:
            return {"error": "Bus not found"}, 404
        db.session.delete(bus)
        db.session.commit()
        return {"message": "Bus removed successfully"}, 200

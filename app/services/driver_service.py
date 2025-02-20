from app.extensions import db
from app.models.bus import Bus
from flask import jsonify

class DriverService:
    @staticmethod
    def add_bus(data):
        new_bus = Bus(driver_id=data['driver_id'], bus_number=data['bus_number'], capacity=data['capacity'], available_seats=data['capacity'])
        db.session.add(new_bus)
        db.session.commit()
        return jsonify({"message": "Bus added successfully"}), 201

    @staticmethod
    def pick_route(data):
        bus = Bus.query.get(data['bus_id'])
        if not bus:
            return jsonify({"error": "Bus not found"}), 404
        bus.route_id = data['route_id']
        db.session.commit()
        return jsonify({"message": "Route assigned successfully"}), 200

    @staticmethod
    def assign_cost(bus_id, data):
        bus = Bus.query.get(bus_id)
        if not bus:
            return jsonify({"error": "Bus not found"}), 404
        bus.ticket_price = data['cost']
        db.session.commit()
        return jsonify({"message": "Ticket price updated"}), 200

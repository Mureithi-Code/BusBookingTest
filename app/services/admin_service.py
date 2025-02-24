from app.extensions import db
from app.models.user import User
from app.models.route import Route
from flask import jsonify

class AdminService:
    @staticmethod
    def remove_driver(driver_id):
        driver = User.query.filter_by(id=driver_id, role="Driver").first()
        if not driver:
            return jsonify({"error": "Driver not found"}), 404
        db.session.delete(driver)
        db.session.commit()
        return jsonify({"message": "Driver removed successfully"}), 200

    @staticmethod
    def cancel_route(route_id):
        route = Route.query.get(route_id)
        if not route:
            return jsonify({"error": "Route not found"}), 404
        db.session.delete(route)
        db.session.commit()
        return jsonify({"message": "Route canceled successfully"}), 200

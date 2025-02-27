from app.extensions import db
from app.models.user import User
from app.models.route import Route
from app.models.message import Message
from app.models.reply import Reply
from flask import jsonify

class AdminService:
    @staticmethod
    def remove_driver(driver_id):
        try:
            print(f"Attempting to remove driver with ID: {driver_id}")

            driver = User.query.filter_by(id=driver_id, role="Driver").first()
            if not driver:
                return {"error": "Driver not found"}, 404

            # Delete related data (routes, messages, etc.)
            from app.models.route import Route
            Route.query.filter_by(driver_id=driver_id).delete()

            from app.models.message import Message
            Message.query.filter((Message.sender_id == driver_id) | (Message.receiver_id == driver_id)).delete()

            db.session.delete(driver)
            db.session.commit()

            return {"message": "Driver removed successfully"}, 200

        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            return {"error": "Internal server error"}, 500

    @staticmethod
    def cancel_route(route_id):
        route = Route.query.get(route_id)
        if not route:
            return jsonify({"error": "Route not found"}), 404
        db.session.delete(route)
        db.session.commit()
        return jsonify({"message": "Route canceled successfully"}), 200
    
    @staticmethod
    def get_all_drivers():
        drivers = User.query.filter_by(role="Driver").all()
        return jsonify([{"id": d.id, "name": d.name, "email": d.email} for d in drivers])

    @staticmethod
    def get_all_routes():
        routes = Route.query.all()
        return jsonify([{"id": r.id, "start": r.start_location, "end": r.end_location, "time": r.departure_time} for r in routes])

    @staticmethod
    def get_all_messages():
        from app.models.message import Message  
        messages = Message.query.all()
        return jsonify([{"id": m.id, "customer_id": m.customer_id, "content": m.content} for m in messages])

    @staticmethod
    def reply_message(message_id, data):
        """
        Admin replies to a customer message.
        Assumes a 'Reply' model linked to 'Message' with a one-to-one relationship.
        """
        message = Message.query.get(message_id)
        if not message:
            return jsonify({"error": "Message not found"}), 404
        
        reply_text = data.get('reply')
        if not reply_text:
            return jsonify({"error": "Reply text is required"}), 400

        # Check if a reply already exists for this message
        if message.reply:
            message.reply.content = reply_text  # Update existing reply
        else:
            reply = Reply(content=reply_text, message_id=message_id)
            db.session.add(reply)

        db.session.commit()
        return jsonify({"message": "Reply sent successfully"}), 200
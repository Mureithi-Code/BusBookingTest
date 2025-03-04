from app.extensions import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)  # Ensures route linkage
    seat_number = db.Column(db.Integer, nullable=False)

    # Status can track changes for audit trail (e.g., rebooking, cancellation, etc.)
    status = db.Column(db.String(20), default="booked")  # Options: booked, canceled, edited

    # Timestamps to track when booking happens or changes
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    customer = db.relationship('User', backref='bookings', lazy=True)
    bus = db.relationship('Bus', backref='bookings', lazy=True)
    route = db.relationship('Route', backref='bookings', lazy=True)

    def __repr__(self):
        return f"<Booking customer {self.customer_id} bus {self.bus_id} seat {self.seat_number} status {self.status}>"

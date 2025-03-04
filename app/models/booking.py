from app.extensions import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(20), default="booked")

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    customer = db.relationship('User', backref='bookings', lazy=True)

    # ⚠️ Fix here — replace backref with back_populates
    bus = db.relationship('Bus', back_populates='bookings', lazy=True)

    route = db.relationship('Route', backref='bookings', lazy=True)

    def __repr__(self):
        return f"<Booking customer {self.customer_id} bus {self.bus_id} seat {self.seat_number} status {self.status}>"

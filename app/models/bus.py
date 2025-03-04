from app.extensions import db

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)   # Total seats
    available_seats = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ticket_price = db.Column(db.Float, nullable=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=True)

    # Relationships
    driver = db.relationship('User', backref='buses')

    # This is good - keep it
    route = db.relationship('Route', backref='buses', foreign_keys=[route_id])

    # New: Relationship to bookings - makes it easy to query all bookings on this bus
    bookings = db.relationship('Booking', backref='bus', lazy=True)

    def __repr__(self):
        return f"<Bus {self.bus_number} - Driver {self.driver_id}>"

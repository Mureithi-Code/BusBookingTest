from app.extensions import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    seat_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="booked")  # booked, canceled

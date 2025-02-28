from app.extensions import db

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bus_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=True)  # link to route
    ticket_price = db.Column(db.Float, nullable=True)  # add ticket price

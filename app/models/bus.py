from app.extensions import db

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ticket_price = db.Column(db.Float, nullable=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=True)  # New column
    driver = db.relationship('User', backref='buses')

    # Optional convenience relationship if you want to easily access the route
    route = db.relationship('Route', backref='buses', foreign_keys=[route_id])

    def __repr__(self):
        return f"<Bus {self.bus_number} - Driver {self.driver_id}>"

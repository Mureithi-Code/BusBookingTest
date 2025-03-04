from app.extensions import db

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_location = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Use back_populates here too
    buses = db.relationship('Bus', back_populates='route', lazy=True)

    price = db.Column(db.Float, nullable=True)
    duration = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Route {self.start_location} to {self.destination}>"

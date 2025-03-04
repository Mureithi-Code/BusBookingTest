from app.extensions import db

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_location = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Add a relationship to buses to easily query all buses on this route
    buses = db.relationship('Bus', backref='route', lazy=True)

    # Optional price and duration fields if you want to display these for customers
    price = db.Column(db.Float, nullable=True)        # Optional, depends on how you handle pricing
    duration = db.Column(db.String(50), nullable=True) # Example: "2 hours 30 minutes"

    def __repr__(self):
        return f"<Route {self.start_location} to {self.destination}>"

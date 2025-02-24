from app.extensions import db

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_location = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))
    cost = db.Column(db.Integer, nullable=False)
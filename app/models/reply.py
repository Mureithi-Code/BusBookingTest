from app.extensions import db

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Back link to the Message (one-to-one relationship)
    message = db.relationship('Message', back_populates='reply')

    def __repr__(self):
        return f"<Reply to message {self.message_id}>"

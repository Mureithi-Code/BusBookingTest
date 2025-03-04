from app.extensions import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    # To support replies, add a parent-child relationship (threading support)
    parent_message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=True)  # For replies
    replies = db.relationship('Message', backref=db.backref('parent_message', remote_side=[id]), lazy=True)

    def __repr__(self):
        return f"<Message from {self.sender_id} to {self.receiver_id}>"

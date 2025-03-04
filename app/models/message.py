from app.extensions import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Self-referential relationship for message threads (optional, if you want threaded messages)
    parent_message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=True)

    # Self-referential relationship for threaded replies (children messages)
    replies = db.relationship('Message', 
                              backref=db.backref('parent_message', remote_side=[id]),
                              lazy=True)

    # One-to-one relationship with Reply (this is the NEW PART you need)
    reply = db.relationship('Reply', back_populates='message', uselist=False)

    def __repr__(self):
        return f"<Message from {self.sender_id} to {self.receiver_id}>"

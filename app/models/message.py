from datetime import datetime
from app.extensions import db  # Importing the initialized SQLAlchemy instance

# Message model

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    seen = db.Column(db.Boolean, default=False)
    chat = db.Column(db.Integer, db.ForeignKey("chat.id"))
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, chat_id, sender_id, content):
        super().__init__()
        self.chat = chat_id
        self.sender_id = sender_id
        self.content = content

    def __repr__(self):
        return f"<Message {self.id}>"
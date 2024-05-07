from datetime import datetime
from app.extensions import db  # Importing the initialized SQLAlchemy instance

# Message model
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # Relationships
    chat = db.relationship("Chat", back_populates="messages")
    sender = db.relationship("User")

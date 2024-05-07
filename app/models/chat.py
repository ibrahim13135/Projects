from datetime import datetime
from app.extensions import db  # Importing the initialized SQLAlchemy instance

# Many-to-many relationship between users and chats
user_chat_association = db.Table(
    'user_chat',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
)

# Chat model
class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Relationships
    messages = db.relationship("Message", back_populates="chat")
    users = db.relationship("User", secondary=user_chat_association, back_populates="chats")


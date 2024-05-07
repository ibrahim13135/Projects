from datetime import datetime
from app.extensions import db  # Importing the initialized SQLAlchemy instance
from .message import Message
class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship(
        'Message',
        primaryjoin='Chat.id == Message.chat',  # This creates the relationship
        backref='message',  # This enables reverse lookup
        lazy='dynamic'  # Loads the chats lazily
    )

    # users is a list of users in the chat
    def __init__(self, user1, user2):
        super().__init__()
        self.user1 = user1.id
        self.user2 = user2.id

    def __repr__(self):
        return f"<Chat {self.id}>"

    @staticmethod
    def exists(user1, user2):
        return Chat.query.filter(
            (Chat.user1 == user1.id) & (Chat.user2 == user2.id) |
            (Chat.user1 == user2.id) & (Chat.user2 == user1.id)
        ).first() is not None;

    @staticmethod
    def send_message(chat_id, sender_id, content):
        message = Message(chat_id, sender_id, content=content)
        db.session.add(message)
        db.session.commit()
        return message

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    chats = db.relationship(
        'Chat',
        primaryjoin='or_(User.id == Chat.user1, User.id == Chat.user2)',  # This creates the relationship
        backref='chat',  # This enables reverse lookup
        lazy='dynamic'  # Loads the chats lazily
    )


    def __init__(self, name, email, password):
        super().__init__()
        self.name = name
        self.email = email
        self.set_password(password)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.name}>"
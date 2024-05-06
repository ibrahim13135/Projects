# app/models/chat.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.extensions import db  # Correct SQLAlchemy reference
from app.models.user import User  # Import User

# Define the Chat model, which represents either one-to-one or group chats
class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=True)  # For group chats
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define one-to-one relationships
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])

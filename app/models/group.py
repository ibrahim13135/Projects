# app/models/group.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.extensions import db  # Correct SQLAlchemy reference
from app.models.user import User  # Import User

# Define the Group model
class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Ensure proper foreign key reference to `User`
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    admin = db.relationship('User', foreign_keys=[admin_id])

    members = db.relationship('User', secondary='group_memberships', backref='groups')

# Define the GroupMembership model
class GroupMembership(db.Model):
    __tablename__ = 'group_memberships'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

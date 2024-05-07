from datetime import datetime
from app.extensions import db  # Importing the initialized SQLAlchemy instance
from .user import user_group_association

# Group model
class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # Establishing the foreign key
    admin = db.relationship("User", back_populates="admin_group")  # Correcting the relationship with User

    # Relationships
    chats = db.Column(db.Integer, db.ForeignKey("chat.id"))

    members = db.relationship(
        "User",
        secondary=user_group_association,
        back_populates="groups"
    )
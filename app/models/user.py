from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

user_group_association = db.Table(
    'user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

# User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, password):
        super().__init__()
        self.name = name
        self.email = email
        self.set_password(password)

    # Other relationships
    chats = db.relationship("Chat", secondary='user_chat', back_populates="users")
    
    groups = db.relationship(
        "Group", secondary=user_group_association, back_populates="members"
    )

    # Relationship for admin group
    admin_group = db.relationship(
        "Group", uselist=False, back_populates="admin"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.name}>"
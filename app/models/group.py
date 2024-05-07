from datetime import datetime
from app.extensions import db

class Membership(db.Model):
    __tablename__ = 'membership'
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Membership {self.group_id}-{self.member_id}>'
# Group model: represents a group in a chat application
class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Group name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation timestamp
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Creator of the group

    # Relationship to the creator of the group (assumes 'User' model exists)
    creator = db.relationship(
        'User',
        primaryjoin='Group.creator_id == User.id',
        backref='created_groups',
    )

    # Relationship to manage group members (many-to-many)
    members = db.relationship(
        'User',
        secondary='membership',  # Associative table for many-to-many relationship
        backref='groups',
    )

    # Relationship to manage messages in the group
    messages = db.relationship(
        'GroupMessage',
        backref='group',
        lazy='dynamic'
    )

    def __init__(self, name, creator):
        self.name = name
        self.creator_id = creator.id

    def __repr__(self):
        return f"<Group {self.name}>"

# GroupMessage model: represents messages sent within a group
class GroupMessage(db.Model):
    __tablename__ = 'group_message'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)  # Group reference
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Sender's ID
    content = db.Column(db.Text, nullable=False)  # Message content
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the message was sent

    # Back-populates
    sender = db.relationship(
        'User',
        backref='sent_group_messages'
    )

    def __repr__(self):
        return f"<GroupMessage {self.id} in Group {self.group_id}>"

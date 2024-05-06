from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, username, message):
        self.username = username
        self.message = message

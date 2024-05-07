# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

# Create the SQLAlchemy instance
db = SQLAlchemy()

# Other extensions
jwt = JWTManager()

socketio = SocketIO(cors_allowed_origins="*")

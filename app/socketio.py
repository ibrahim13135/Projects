# app/socketio.py
from flask_socketio import SocketIO, emit, join_room, leave_room
from app.extensions import socketio
from app.models.message import Message  # If you store chat messages
from app.extensions import db

@socketio.on("join")
def on_join(data):
    chat_id = data.get("chat_id")
    # Join the Socket.IO room using chat_id
    socketio.join_room(str(chat_id))
    # Optionally, you can send a welcome message or some other response

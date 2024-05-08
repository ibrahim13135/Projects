# app/socketio.py
from app.extensions import socketio
from app.models.message import Message
from app.extensions import db

@socketio.on("join_room")
def join_room(data):
    print("Joining room...")
    chat_id = data.get("chat_id")
    socketio.join_room(str(chat_id))

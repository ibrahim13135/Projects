# app/socketio.py
from flask_socketio import SocketIO, emit, join_room, leave_room
from app.extensions import socketio
from app.models.message import Message  # If you store chat messages
from app.extensions import db

# Event when a user joins a room
@socketio.on('join')
def handle_join(data):
    room = data['room']
    username = data['username']
    join_room(room)
    emit('message', {'msg': f'{username} has joined the room.'}, to=room)

# Event when a user leaves a room
@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    username = data['username']
    leave_room(room)
    emit('message', {'msg': f'{username} has left the room.'}, to=room)

# Event when a user sends a message
@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    content = data['content']
    sender_id = data['sender_id']  # Assuming you have sender info

    # If storing messages, you can add it to the database
    message = Message(chat_id=room, sender_id=sender_id, content=content)
    db.session.add(message)
    db.session.commit()

    # Broadcast the message to everyone in the room
    emit('message', {'msg': content, 'sender_id': sender_id}, to=room)

# app/socketio.py
from flask_socketio import emit, join_room, leave_room
from app.extensions import socketio
from app.extensions import db
from app.models import Message

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'msg': f'{data["username"]} has joined the room.'}, to=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f'{data["username"]} has left the room.'}, to=room)

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    sender_id = data['sender_id']
    message_content = data['content']

    message = Message(chat_id=room, sender_id=sender_id, content=message_content)
    db.session.add(message)
    db.session.commit()

    emit('message', {'msg': message_content, 'sender_id': sender_id}, to=room)

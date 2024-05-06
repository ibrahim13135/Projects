# app/routes/chat.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.chat import Chat
from app.models.message import Message
from app.extensions import db, socketio

chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_chat():
    data = request.get_json()
    user_id = get_jwt_identity()
    other_user_id = data.get("other_user_id")

    # Create a one-to-one chat
    chat = Chat(user1_id=user_id, user2_id=other_user_id)
    db.session.add(chat)
    db.session.commit()

    return jsonify({"chat_id": chat.id}), 201

@chat_blueprint.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    chat_id = data.get("chat_id")
    sender_id = get_jwt_identity()
    content = data.get("content")

    message = Message(chat_id=chat_id, sender_id=sender_id, content=content)
    db.session.add(message)
    db.session.commit()

    # Broadcast the message to the chat room via Socket.IO
    socketio.emit("message", {"chat_id": chat_id, "sender_id": sender_id, "content": content}, room=str(chat_id))

    return jsonify({"message": "Message sent"}), 201

@chat_blueprint.route('/receive', methods=['GET'])
@jwt_required()
def receive_messages():
    chat_id = request.args.get("chat_id")
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()

    return jsonify([{"id": msg.id, "sender_id": msg.sender_id, "content": msg.content, "timestamp": msg.timestamp} for msg in messages]), 200

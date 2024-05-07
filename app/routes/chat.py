# app/routes/chat.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.chat import Chat
from app.models.user import User
from app.models.message import Message
from app.extensions import db, socketio

chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_chat():
    data = request.get_json()
    sender_id = get_jwt_identity()
    user_email = data.get("with")

    user1 = User.query.get(sender_id)
    user2 = User.query.filter_by(email=user_email).first()

    if not user2:
        return jsonify({"message": "User not found"}), 404

    # Create a one-to-one chat
    if Chat.exists(user1, user2):
        return jsonify({"message": "Chat already exists"}), 400

    chat = Chat(user1, user2)
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

    # Sending the message in the chat
    message = Message(chat_id=chat_id, sender_id=sender_id, content=content)
    db.session.add(message)
    db.session.commit()

    # Emit the message to the Socket.IO room associated with this chat
    socketio.emit(
        "new_message",
        {
            "chat_id": chat_id,
            "sender_id": sender_id,
            "content": content,
            "timestamp": message.timestamp.isoformat()  # ISO format for easy parsing
        },
        room=str(chat_id)  # Emit to the specific chat room
    )

    return jsonify({"message": "Message sent"}), 201


@chat_blueprint.route('/list', methods=['GET'])
@jwt_required()
def list_chats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    chats = user.chats

    return jsonify(
        {
            "chats": [
                {
                    "id": chat.id,
                    "user1": chat.user1,
                    "user2": chat.user2,
                    "created_at": chat.created_at,
                }
                for chat in chats
            ],
        }
    ), 200

@chat_blueprint.route('/receive', methods=['GET'])
@jwt_required()
def receive_messages():
    data = request.get_json()
    chat_id = data.get("chat_id")
    chat = Chat.query.get(chat_id)
    messages = chat.messages

    return jsonify(
        {
            "messages": [
                {
                    "id": message.id,
                    "sender_id": message.sender_id,
                    "content": message.content,
                    "timestamp": message.timestamp,
                }
                for message in messages
            ],
        }
    ), 200
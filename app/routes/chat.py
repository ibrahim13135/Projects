# app/routes/chat.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.chat import Chat
from app.models.user import User
from app.models.message import Message
from app.extensions import db, socketio

chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/create', methods=['POST'])
@jwt_required(locations=['headers'])
def create_chat():
    data = request.get_json()
    sender_id = get_jwt_identity()
    user_email = data.get("withEmail")
    user1 = User.query.get(sender_id)
    user2 = User.query.filter_by(email=user_email).first()

    if not user2:
        return jsonify(), 404

    # Create a one-to-one chat
    if Chat.exists(user1, user2):
        return jsonify(), 400

    chat = Chat(user1, user2)
    db.session.add(chat)
    db.session.commit()

    this_chat = user1.chats.filter((Chat.id == chat.id)).first()

    return jsonify({
        "id": this_chat.id,
        "user1": this_chat.user1,
        "user2": this_chat.user2,
        "users": this_chat.users,
        "created_at": this_chat.created_at,
        "messages":  [
            {
                "id": message.id,
                "chat": message.chat,
                "sender_id": message.sender_id,
                "content": message.content,
                "seen": message.seen,
                "timestamp": message.timestamp
            }
            for message in this_chat.messages.all()
        ]
    }), 201

@chat_blueprint.route('/send', methods=['POST'])
@jwt_required(locations=['headers'])
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

    return jsonify({
        "id": message.id,
        "chat": message.chat,
        "sender_id": message.sender_id,
        "content": message.content,
        "seen": message.seen,
        "timestamp": message.timestamp  # ISO format for easy parsing
    }), 201


@chat_blueprint.route('/list', methods=['GET'])
@jwt_required(locations=['headers'])
def list_chats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(), 404
    chats = user.chats.all()

    return jsonify(
        {
            "chats": [
                {
                    "id": chat.id,
                    "user1": chat.user1,
                    "user2": chat.user2,
                    "users": chat.users,
                    "created_at": chat.created_at,
                    "messages": [
                        {
                            "id": message.id,
                            "chat": message.chat,
                            "sender_id": message.sender_id,
                            "content": message.content,
                            "seen": message.seen,
                            "timestamp": message.timestamp
                        }
                        for message in chat.messages.all()
                    ]
                }
                for chat in chats
            ]
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
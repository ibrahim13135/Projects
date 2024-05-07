# app/routes/group.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.chat import Chat
from app.models.group import Group
from app.models.message import Message
from app.extensions import db, socketio

group_blueprint = Blueprint('group', __name__)

@group_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_group():
    data = request.get_json()
    admin_id = get_jwt_identity()
    name = data.get("name")

    group = Group(name=name, admin_id=admin_id)
    db.session.add(group)
    db.session.commit()

    return jsonify({"group_id": group.id}), 201

@group_blueprint.route('/join', methods=['POST'])
@jwt_required()
def join_group():
    data = request.get_json()
    group_id = data.get("group_id")
    user_id = get_jwt_identity()

    # membership = GroupMembership(group_id=group_id, user_id=user_id)
    # db.session.add(membership)
    # db.session.commit()

    return jsonify({"message": "User joined the group"}), 201

@group_blueprint.route('/send', methods=['POST'])
@jwt_required()
def send_group_message():
    data = request.get_json()
    group_id = data.get("group_id")
    sender_id = get_jwt_identity()
    content = data.get("content")

    message = Message(chat_id=group_id, sender_id=sender_id, content=content)
    db.session.add(message)
    db.session.commit()

    # Broadcast the message to the group room via Socket.IO
    socketio.emit("message", {"group_id": group_id, "sender_id": sender_id, "content": content}, room=str(group_id))

    return jsonify({"message": "Message sent to group"}), 201

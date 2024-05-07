# app/routes/group.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.group import Group, GroupMessage
from app.models.user import User


group_blueprint = Blueprint('group', __name__)


# Route to create a new group
@group_blueprint.route('/create', methods=['POST'])
@jwt_required()  # Ensure user is authenticated
def create_group():
    current_user_id = get_jwt_identity()  # Get the authenticated user's ID
    group_name = request.json.get('name', '')  # Get the group name from the request
    print(group_name)
    if not group_name:
        return jsonify({'error': 'Group name is required'}), 400

    # Create a new group with the current user as the creator
    current_user = User.query.get(current_user_id)
    new_group = Group(name=group_name, creator=current_user)
    new_group.members.append(current_user)  # Add the creator to the group
    
    db.session.add(new_group)
    db.session.commit()

    return jsonify({'message': 'Group created successfully', 'group': new_group.id}), 201


# Route to add a member to a group
@group_blueprint.route('/<int:group_id>/add_member', methods=['POST'])
@jwt_required()
def add_member_to_group(group_id):
    current_user_id = get_jwt_identity()
    user_id = request.json.get('user_id')  # ID of the user to add to the group
    
    group = Group.query.get(group_id)

    if not group:
        return jsonify({'error': 'Group not found'}), 404

    if group.creator_id != current_user_id:
        return jsonify({'error': 'Only the group creator can add members'}), 403
    
    # if user is in the group
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user in group.members:
        return jsonify({'error': 'User is already a member of the group'}), 400


    group.members.append(user)
    db.session.commit()

    return jsonify({'message': 'Member added successfully'}), 200


# Route to send a message to a group
@group_blueprint.route('/<int:group_id>/send', methods=['POST'])
@jwt_required()
def send_message_to_group(group_id):
    current_user_id = get_jwt_identity()
    content = request.json.get('content')  # Message content
    
    if not content:
        return jsonify({'error': 'Message content is required'}), 400

    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    # Create a new GroupMessage and add it to the group
    message = GroupMessage(group_id=group_id, sender_id=current_user_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully', 'message_id': message.id}), 201


# Route to list all groups a user is part of
@group_blueprint.route('/my_groups', methods=['GET'])
@jwt_required()
def list_my_groups():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # List all groups the user is part of
    groups = [{'id': g.id, 'name': g.name, 'creator': g.creator_id} for g in user.groups]

    return jsonify(groups), 200
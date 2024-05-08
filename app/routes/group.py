# app/routes/group.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.group import Group, GroupMessage
from app.models.user import User


group_blueprint = Blueprint('group', __name__)


# Route to create a new group
@group_blueprint.route('/create', methods=['POST'])
@jwt_required(locations=['headers'])
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

    # return all the groups details
    return jsonify({
        'id': new_group.id,
        'name': new_group.name,
        'creator_id': new_group.creator_id,
        'created_at': new_group.created_at,
        'members': [
            {'id': member.id, 'name': member.name, 'email': member.email} for member in new_group.members
        ],
        'messages': [
            {'id': message.id, 'sender_id': message.sender_id, 'content': message.content, 'timestamp': message.timestamp}
            for message in new_group.messages
        ]
    }), 201

# Route to add a member to a group
@group_blueprint.route('/<int:group_id>/add_member', methods=['POST'])
@jwt_required(locations=['headers'])
def add_member_to_group(group_id):
    current_user_id = get_jwt_identity()
    new_member_email = request.json.get('email')
    group = Group.query.get(group_id)

    if not new_member_email:
        return jsonify({'error': 'Email is required'}), 400

    if not group:
        return jsonify({'error': 'Group not found'}), 404

    if group.creator_id != current_user_id:
        return jsonify({'error': 'Only the group creator can add members'}), 403
    
    new_member = User.query.filter_by(email=new_member_email).first()
    if not new_member:
        return jsonify({'error': 'User not found'}), 404
    
    if new_member in group.members:
        return jsonify({'error': 'User is already a member of the group'}), 400
    
    group.members.append(new_member)

    db.session.commit()

    # return this member's details
    return jsonify({
        'id': new_member.id,
        'name': new_member.name,
        'email': new_member.email
    }), 200


# Route to send a message to a group
@group_blueprint.route('/<int:group_id>/send', methods=['POST'])
@jwt_required(locations=['headers'])
def send_message_to_group(group_id):
    current_user_id = get_jwt_identity()
    content = request.json.get('content')  # Message content
    

    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'User not exist'}), 404

    if not content:
        return jsonify({'error': 'Message content is required'}), 400

    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    
    if user not in group.members:
        return jsonify({'error': 'You are not a member of this group'}), 403

    # Create a new GroupMessage and add it to the group
    message = GroupMessage(group_id=group_id, sender_id=current_user_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({
        'id': message.id,
        'sender_id': message.sender_id,
        'content': message.content,
        'timestamp': message.timestamp,
    }), 201

# Route to list all groups a user is part of
@group_blueprint.route('/my_groups', methods=['GET'])
@jwt_required(locations=['headers'])
def list_my_groups():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    groups = [
        {
            'id': group.id,
            'name': group.name,
            'creator_id': group.creator_id,
            'created_at': group.created_at,
            'members': [
                {'id': member.id, 'name': member.name, 'email': member.email} for member in group.members
            ],
            'messages': [
                {'id': message.id, 'sender_id': message.sender_id, 'content': message.content, 'timestamp': message.timestamp}
                for message in group.messages
            ]
        }
        for group in user.groups
    ]

    return jsonify(groups), 200


# Route to delete a group
@group_blueprint.route('/<int:group_id>/delete', methods=['DELETE'])
@jwt_required(locations=['headers'])
def delete_group(group_id):
    current_user_id = get_jwt_identity()

    group = Group.query.get(group_id)

    if not group:
        return jsonify({'error': 'Group not found'}), 404

    if group.creator_id != current_user_id:
        return jsonify({'error': 'Only the group creator can delete the group'}), 403
    
    # get all the group messages and delete them
    messages = group.messages
    for message in messages:
        db.session.delete(message)

    # delete the group and it Memberships and GroupMessages
    # memberships = group.members
    # for membership in memberships:
    #     db.session.delete(membership)
    

    db.session.delete(group)
    db.session.commit()

    return jsonify({'message': 'Group deleted successfully'}), 200
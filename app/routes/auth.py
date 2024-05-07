# app/routes/auth.py
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(
        name,
        email,
        password,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    print(user.email)

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)

    # Set the JWT in a secure cookie
    response = make_response(jsonify({"message": "Login successful"}))
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
    )
    
    return response

@auth_blueprint.route('/me', methods=['GET'])
@jwt_required(locations=["cookies"])  # Tell Flask-JWT-Extended to look for JWT in cookies
def get_current_user():
    user_id = get_jwt_identity()  # Extract user identity from the JWT
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
    }), 200

@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required(locations=["cookies"])
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    response.set_cookie("access_token", "", expires=0)
    return response

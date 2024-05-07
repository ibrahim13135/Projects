# app/__init__.py
from flask import Flask
from .extensions import db, jwt, socketio
from .config import Config
from flask_cors import CORS

# Ensure blueprints are imported correctly
from .routes.auth import auth_blueprint
from .routes.chat import chat_blueprint
from .routes.group import group_blueprint  # Import all blueprints

def create_app():
    app = Flask(__name__)
    CORS(
        app,
        origins=["http://localhost:5173"],
        methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        # access cookies from the frontend
        allow_headers=["Content-Type", "Authorization", "Cookie"],
        supports_credentials=True,
    )
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        db.create_all()

    jwt.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(chat_blueprint, url_prefix="/chat")
    app.register_blueprint(group_blueprint, url_prefix="/group")

    return app

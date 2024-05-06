from flask import Flask
from .extensions import db, jwt, socketio
from .config import Config
from .routes import auth_blueprint, chat_blueprint, group_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(chat_blueprint, url_prefix='/chat')
    app.register_blueprint(group_blueprint, url_prefix='/group')

    return app

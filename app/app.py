from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from config import AppConfig
from models import db
from models import ChatMessage


app = Flask(__name__, static_folder='static')
app.config.from_object(AppConfig)
db.init_app(app)  # Initialize the database

socketio = SocketIO(cors_allowed_origins='*')
socketio.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@socketio.on('connect')
def handle_connect():
    print('Client is online')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client is offline')


@socketio.on('message')
def handle_message(json):
    message = ChatMessage(username=json['username'], message=json['message'])
    db.session.add(message)
    db.session.commit()
    emit('message', message.__dict__, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)

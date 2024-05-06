from flask import Flask
from flask_socketio import SocketIO, emit
from app.models import Chat_Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('connect')
def handle_connect():
    print('Client is online')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client is offline')


@socketio.on('message')
def handle_message(json):
    message = Chat_Message(message=json['message'], username=json['username'])
    emit('message', message.__dict__, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)

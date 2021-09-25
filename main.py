from flask import Flask, render_template
from flask_socketio import SocketIO, emit

async_mode = None
app = Flask(__name__)
socket_ = SocketIO(app)

@app.route('/')

def index():
    return render_template('test.html')


@app.route('/blabla')
def blabla():
    return render_template('blabla.html')

@socket_.on('connect')
def test_connect():
    emit('chat message','Hafti Abi Babi Strassenstyle.')
    print('user connected')

@socket_.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socket_.on('chat message')
def test_message(message):
    emit('chat message', message, broadcast=True)
if __name__ == '__main__':
    socket_.run(app, debug=True, host='0.0.0.0')
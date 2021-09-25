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


if __name__ == '__main__':
    socket_.run(app, debug=True)
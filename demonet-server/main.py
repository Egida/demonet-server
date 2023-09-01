import sys
from threading import Thread
import asyncio
from time import sleep

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from functions.connections import Connections

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

connection = Connections(host="zacsucks.local", port=60123)

def start_connection():
    asyncio.run(connection.start_server())

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print(f"Receieved message from client: {message}")
    response = "Message received: " + message
    emit('response', response)

@socketio.on('command')
def handle_command(command):
    print(f"Received command from client: {command}")
    # Forward the command to all connected clients through SSL socket
    connection.show_conns()
    connection.send_message(command)

def main():
    thread = Thread(target=start_connection)
    thread.daemon = True
    thread.start()
    sleep(3)
    socketio.run(app, port=5001, debug=False)
try:
    if __name__ == '__main__':
        main()
except Exception as e:
    print('Interrupt detected')
finally:
    print('Hmmmmmm')
    sys.exit(0)
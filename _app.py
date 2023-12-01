from flask import Flask, request
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
socketio = SocketIO(app)

@app.route('/')
def index():
    return "ESP8266 SocketIO Server"

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('event_name')
def handle_my_custom_event(json_data):
    print('received json:', json_data)
    # You can process the data here and even send a response back to ESP8266
    emit('response_event', {'data': 'Response from server'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import json
import psycopg2
import pandas as pd

# Connecting to DB
def connect_sql(username, password, host, database):
    conn = psycopg2.connect(host=host, database=database, user=username, password=password)
    return conn

sql_host="ec2-44-206-18-218.compute-1.amazonaws.com"
sql_username="qoxrlnvnhoqxrj"
sql_password="3b0361f995fa7559058fdaba03058de268ee13a7cda5b27bbe17ddc4c8a4c5ff"
sql_database="d5js1h474dsr6k"

def add_user(username, password, host, database):
    conn = psycopg2.connect(host=host, database=database, user=username, password=password)
    curs = conn.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
socketio = SocketIO(app)

latest_packet = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('event_name')
def handle_my_custom_event(json_data):
    global latest_packet
    print('received json:', json_data)
    latest_packet = json_data  # Update the latest packet
    emit('update_packet', latest_packet, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)

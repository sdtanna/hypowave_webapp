from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import json
import psycopg2
import pandas as pd
import pytz
import os

import datetime #ADD THIS TO REQS.TXT

DATABASE_URL = os.environ['DATABASE_URL']
LOCAL = False

# Connecting to DB
def connect_sql():
    if LOCAL:
        cardentials = get_credentials('super_secert_passwords.txt')
        sql_host = cardentials['host']
        sql_username = cardentials['username']
        sql_password = cardentials['password']
        sql_database = cardentials['database']

        conn=psycopg2.connect(host=sql_host, database=sql_database, user=sql_username, password=sql_password)
        return conn
    else:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn


def get_credentials(filename):
    credentials = {}
    with open(filename, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials


def add_user(data):
    conn = connect_sql()
    curs = conn.cursor()

    try:
        query = """SELECT u_id, u_name, u_pass, u_email FROM user_data;"""
        curs.execute(query)
        user_data = curs.fetchall()
        user_data = pd.DataFrame(user_data, dtype = "string")
        user_data.columns = ['u_id', 'u_name', 'u_pass', 'u_email']
        conn.commit()

        if ((data[1] in user_data['u_name'].values) == False):
            curs.execute("""INSERT INTO user_data(u_name, u_pass, u_email)
                        VALUES (%s, %s, %s);""", (data[0], data[1], data[2]))
            print("good1")
        
    except:
        curs.execute("""INSERT INTO user_data(u_name, u_pass, u_email)
                    VALUES (%s, %s, %s);""", (data[0] + '1', data[1] + '1', data[2] + '1'))
        print("good2")

def save_trackdata(data, date, sensor, room, time):
    conn = connect_sql()
    curs = conn.cursor()

    try:
        for i in data:
            trackid = i[0]
            xpos = i[1]
            ypos = i[2]
            curs.execute("""INSERT INTO historical(track_id, x_pos, y_pos, date, s_id, r_id, time) VALUES (%s, %s, %s, %s, %s, %s, %s);""", (trackid, xpos, ypos, date, sensor, room, time))
        conn.commit()  # Commit the transaction
    except Exception as e:
        print("That did not work")
        print(e)  # Print the exception
    finally:
        curs.close()  # Close the cursor
        conn.close()  # Close the connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
socketio = SocketIO(app, ping_timeout=10, ping_interval=5)

latest_packet = None

@app.route("/", methods = ["GET", "POST"])

def home():
    if request.method == "POST":        
        if request.form['action'] == 'adduser':
            username = 'User1'
            userpass = 'User1Pass'
            useremail = 'User1Email'

            newUserData = (username, userpass, useremail)
            add_user(newUserData)
            print("fdone")
        
        if request.form['action'] == 'startSensor':
            socketio.emit('command', {'data':'startSensor'})

        if request.form['action'] == 'stopSensor':
            socketio.emit('command', {'data':'stopSensor'})

        if request.form['action'] == 'resetSensor':
            socketio.emit('command', {'data':'resetSensor'})

        if request.form['action'] == 'sendCmd':
            cmd_to_send = request.form.get("cmdinput")
            socketio.emit('command', {'data':cmd_to_send})


        else:
            return ('', 204)
    
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)
    

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('sensor_datapacket_1')
def handle_my_custom_event(json_data):
    global latest_packet
    print('received json:', json_data)
    latest_packet = json_data  # Update the latest packet
    emit('update_packet', latest_packet, broadcast=True)

    frameNum = int(json_data['frameNum'])

    if 'trackData' in json_data:
        data_to_add = [(entry[0], entry[1], entry[2]) for entry in json_data['trackData']]
        now = datetime.datetime.now(pytz.timezone('US/Eastern'))
        formatted_date = now.strftime('%Y-%m-%d')
        formatted_time = now.strftime('%H:%M:%S')

        if frameNum % 10 == 0:
            save_trackdata(data_to_add, formatted_date, 1, 1, formatted_time)

@socketio.on('send_command')
def handle_send_command(command):
    # Emit a command event to the client
    emit('command', {'command': command})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
    save_trackdata("test", "test", "test", "test", "test")
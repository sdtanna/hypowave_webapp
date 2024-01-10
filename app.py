from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import json
import psycopg2
import pandas as pd

import datetime #ADD THIS TO REQS.TXT

# Connecting to DB
def connect_sql(username, password, host, database):
    conn = psycopg2.connect(host=host, database=database, user=username, password=password)
    return conn

sql_host="ec2-44-206-18-218.compute-1.amazonaws.com"
sql_username="qoxrlnvnhoqxrj"
sql_password="3b0361f995fa7559058fdaba03058de268ee13a7cda5b27bbe17ddc4c8a4c5ff"
sql_database="d5js1h474dsr6k"

#conn = psycopg2.connect(host=sql_host, database=sql_database, user=sql_username, password=sql_password)
#curs = conn.cursor()

# Print data in user_data 

#query = """SELECT u_id, u_name, u_pass, u_email FROM user_data;"""
#curs.execute(query)
#user_data = curs.fetchall()
#user_data = pd.DataFrame(user_data, dtype = "string")
###user_data.columns = ['u_id', 'u_name', 'u_pass', 'u_email']
#print(user_data.to_string())

#curs.execute("""SELECT column_name FROM information_schema.columns WHERE table_name = 'historical'""")
#for table in curs.fetchall():
#    print(table)

#curs.execute("""INSERT INTO user_data(u_name, u_pass, u_email) VALUES (%s, %s, %s);""", ("1", "1", "1"))
#print("good1")

#curs.execute("""SELECT u_name FROM user_data WHERE u_name=%s""", ("1"))
#for table in curs.fetchall():
#    print(table)
#print("good1")

#conn.commit()


# Function adds user when user icon clicked - to be changed
def add_user(username, password, host, database, data):
    conn = psycopg2.connect(host=host, database=database, user=username, password=password)
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

def save_trackdata(username, password, host, database, data, date, sensor, room, time):
    conn = psycopg2.connect(host=host, database=database, user=username, password=password)
    curs = conn.cursor()

    try:
        for i in data:
            xpos = i[0]
            ypos = i[1]
            curs.execute("""INSERT INTO historical(x_pos, y_pos, date, s_id, r_id, time) VALUES (%f, %f, %s, %d, %d, %s);""", (xpos, ypos, date, sensor, room, time))
    except:
        print("That did not work")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
socketio = SocketIO(app)

latest_packet = None

@app.route("/", methods = ["GET", "POST"])

def home():
    if request.method == "POST":        
        if request.form['action'] == 'adduser':
            username = 'User1'
            userpass = 'User1Pass'
            useremail = 'User1Email'

            newUserData = (username, userpass, useremail)
            add_user(sql_username, sql_password, sql_host, sql_database, newUserData)
            print("fdone")

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

    if 'trackData' in json_data:
        data_to_add = [(entry[1], entry[2]) for entry in json_data['trackData']]
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d')
        formatted_time = now.strftime('%H:%M:%S')

        #save_trackdata(sql_username, sql_password, sql_host, sql_database, data_to_add, formatted_date, 1, 1, formatted_time)

        

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)

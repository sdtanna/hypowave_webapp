import psycopg2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import random
import matplotlib.colors as mcolors
from PIL import Image

def generate_heatmap(username, password, host, database, start_date_str, end_date_str):
    #Parse the date strings
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    #Define the detection space dimensions
    DETECTION_SPACE_DIMENSIONS = (196, 441)  #in meters
    GRANULARITY = 2  #in meters

    #Compute the dimensions of the heatmap
    xdim = int(DETECTION_SPACE_DIMENSIONS[0] / GRANULARITY)
    ydim = int(DETECTION_SPACE_DIMENSIONS[1] / GRANULARITY)

    #Connect to your postgres database
    conn = psycopg2.connect(host=host, database=database, user=username, password=password)

    #Create a cursor object
    cur = conn.cursor()

    #Define your time range (Opening Hours from 11am - 5pm)
    start_time = datetime.strptime('11:00:00', '%H:%M:%S').time()
    end_time = datetime.strptime('17:00:00', '%H:%M:%S').time()

    #Query the database
    query = f"SELECT x_pos, y_pos FROM your_table WHERE date >= '{start_date}' AND date <= '{end_date}' AND time >= '{start_time}' AND time <= '{end_time}'"
    cur.execute(query)
    rows = cur.fetchall()

    #Initialize a 2D vector for the heatmap
    heatmap_data = np.zeros((xdim, ydim))

    #Process the rows
    for row in rows:
        x, y = row
        #Round the coordinates to the correct space             #I.e. x,y = 2.7, 7.9
        x_index = min(int(x / GRANULARITY), xdim - 1)           #min(int(2.7 / 0.5), 11) = min(5, 11) = 5
        y_index = min(int(y / GRANULARITY), ydim - 1)           #min(int(7.9 / 0.5), 27) = min(15, 27) = 15
    
        #Increase the frequency in the corresponding index
        heatmap_data[x_index][y_index] += 1                     #Increment the frequency count at (5, 15). Index 5 represents space from 2.5m - 3m, Index 15 represents space from 7.5m - 8m

    #Close the cursor and connection
    cur.close()
    conn.close()

    #Create a colormap that represents the color spectrum you specified with transparency
    colors = ['navy', 'blue', 'green', 'yellow', 'red']
    cmap = mcolors.LinearSegmentedColormap.from_list('custom_cmap', colors)

    #Convert the colormap to RGBA colors
    cmap = cmap(np.arange(cmap.N))

    #Apply the alpha gradient to the colormap
    alphas = np.linspace(0.1, 1, cmap.shape[0])
    cmap[:,-1] = alphas

    #Load and resize the floor plan
    floor_plan = Image.open('floor_plan.png')
    floor_plan = floor_plan.resize((ydim, xdim))  # Resize to match heatmap dimensions

    #Create a new figure
    plt.figure()

    #Display the resized floor plan
    plt.imshow(floor_plan)

    #Display the heatmap on top of the floor plan
    sns.heatmap(heatmap_data, cmap=mcolors.ListedColormap(cmap), alpha=0.5)

    #Show the plot
    plt.show()

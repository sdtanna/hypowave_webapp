import numpy as np
import matplotlib.pyplot as plt
import random
import psycopg2
from datetime import datetime
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable

def generate_heatmap(data):

    # Define the detection space dimensions
    WIDTH = 5
    LENGTH = 8
    SCALE = 2
    DETECTION_SPACE_DIMENSIONS = (WIDTH*SCALE, LENGTH*SCALE)  # in meters
    GRANULARITY = .5  # in meters
    NORMALIZATION_FACTOR = 0.1  # What % of least dense data should be normalized to zero (neglected)

    # Compute the dimensions of the heatmap
    xdim = int(DETECTION_SPACE_DIMENSIONS[0] / GRANULARITY)
    ydim = int(DETECTION_SPACE_DIMENSIONS[1] / GRANULARITY)

    # Initialize a 2D vector for the heatmap
    heatmap_data = np.zeros((xdim, ydim))

    # Process the rows
    for row in data:
        x, y = row
        # Check if the data is within the detection range
        if 0 <= x < DETECTION_SPACE_DIMENSIONS[0] and 0 <= y < DETECTION_SPACE_DIMENSIONS[1]:
            # Round the coordinates to the correct space
            x_index = min(int(x / GRANULARITY), xdim - 1)
            y_index = min(int(y / GRANULARITY), ydim - 1)
            
            # Increase the frequency in the corresponding index
            heatmap_data[x_index][y_index] += 1
    
    # Normalize the heatmap data to the range [0, 1]
    heatmap_data = heatmap_data / np.max(heatmap_data)

    # Set all values below Normalization factor to 0
    heatmap_data = np.where(heatmap_data < NORMALIZATION_FACTOR, 0, heatmap_data)

    # Create a custom colormap that starts with a transparent color and ends with the colors you specified
    colors = [(0, 0, 0, 0), 'navy', 'blue', 'green', 'yellow', 'red']  # R -> G -> B -> A
    cmap_name = 'custom_cmap'
    cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=1000)

    # Modify the alpha channel of the colormap
    cmap._init()
    alphas = np.linspace(0, 1, cmap.N+3)
    cmap._lut[:,-1] = np.concatenate([np.zeros(int((cmap.N+3)*0.01)), alphas[int((cmap.N+3)*0.01):]])

    # Load and resize the floor plan
    floor_plan = Image.open('floor.png')
    floor_plan = floor_plan.resize((ydim, xdim))  # Resize to match heatmap dimensions

    # Create a new figure
    fig, ax = plt.subplots()

    # Display the resized floor plan
    ax.imshow(floor_plan)

    # Display the heatmap on top of the floor plan
    img = ax.imshow(heatmap_data, cmap=cmap, interpolation='nearest')

    # Remove the axes
    plt.axis('off')

    # Save the plot without the colorbar
    plt.savefig('heatmap_no_axes.png', bbox_inches='tight', pad_inches=0, dpi=300)

    # Show the plot
    # plt.show()

    # Open the images
    floor_plan2 = Image.open('floor_plan2.png')
    heatmap_no_axes = Image.open('heatmap_no_axes.png')

    # Resize the heatmap to the size of the specific area (replace 'width' and 'height' with the actual size)
    width = int(floor_plan2.width * 0.75)
    height = int(floor_plan2.height * 0.72)
    heatmap_no_axes = heatmap_no_axes.resize((width, height))

    left = (floor_plan2.width - heatmap_no_axes.width) // 2
    upper = (floor_plan2.height - heatmap_no_axes.height) // 2
    right = left + heatmap_no_axes.width
    lower = upper + heatmap_no_axes.height
    position = (left, upper, right, lower)

    # Create a new image with the same size as floor_plan2
    new_image = floor_plan2.copy()

    # Paste the heatmap onto the new image
    new_image.paste(heatmap_no_axes, position, heatmap_no_axes)

    # Save the new image
    new_image.save('new_image.png')

    # Create a new figure for the colorbar
    fig = plt.figure(figsize=(1, 6))

    # Create a new Axes object for the colorbar
    # (Move to Right, Move Upwards, Make Wider, Make Taller)
    cax = fig.add_axes([0.05, 0.2, 1.2, 1.1])

    # Create a ScalarMappable with the same colormap as the heatmap
    sm = ScalarMappable(cmap=cmap, norm=Normalize(vmin=0, vmax=1))

    # Add the colorbar to the Axes object
    cbar = fig.colorbar(sm, cax=cax, orientation='vertical')

    # Set the tick locations
    cbar.set_ticks([0, 0.5, 1])

    # Set the tick labels
    cbar.set_ticklabels(['Low\nDensity', 'Moderate\nDensity', 'High\nDensity'])

    # Save the colorbar
    plt.savefig('colorbar.png', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

    # Open the images
    new_image = Image.open('new_image.png')
    colorbar = Image.open('colorbar.png')

    # Concatenate the images
    final_image = Image.new('RGB', (new_image.width + colorbar.width, new_image.height))
    final_image.paste(new_image, (0, 0))
    final_image.paste(colorbar, (new_image.width, 0))

    # Save the final image
    final_image.save('heatmap.png')
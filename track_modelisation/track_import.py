import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon



def import_circuit_from_csv(filepath):
    try:
        df = pd.read_csv(filepath) 
        return df # returns a df with de center line of the track
    except Exception as e:
        print(f"Error importing circuit from {filepath}: {e}")
        return None


def compute_borders(df):
    if df is None or df.empty:
        print("DataFrame is empty or None.")
        return None
    
    center_line = np.array(df[['x', 'y']])
    print("Center line points:", center_line)
    left_borders = []
    right_borders = []
    width = 10  # Example width of the track 

    for i in range(len(center_line) - 1):
        dx = center_line[i + 1][0] - center_line[i][0]
        dy = center_line[i + 1][1] - center_line[i][1]
        length = np.sqrt(dx**2 + dy**2)
        
        if length == 0:
            continue # Skip if the segment length is zero
        
        nx = dy / length * (width / 2) ; ny = -dx / length * (width / 2) ; 

        # (dy, -dx) gives the normal vector to the segment, normalized it to the desired width

        right_borders.append([center_line[i][0] + nx, center_line[i][1] + ny]) #add the normal vector to the right side
        left_borders.append([center_line[i][0] - nx, center_line[i][1] - ny]) #soustract the normal vector to the left side
    
    return right_borders, left_borders


def plot_track(right_borders, left_borders):
    if right_borders is None or left_borders is None:
        print("Right or left borders are None.")
        return
    
    right_borders = np.array(right_borders)
    left_borders = np.array(left_borders)
    
    plt.figure(figsize=(10, 10))
    plt.plot(right_borders[:, 0], right_borders[:, 1], label='right Border', color='blue')
    plt.plot(left_borders[:, 0], left_borders[:, 1], label='Left Border', color='red')
    plt.title('Track Borders')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.axis('equal')
    plt.grid()
    plt.show()



def linestring_from_center(center_line):
    if center_line is None or center_line.empty:
        print("Center line is empty or None.")
        return None
    
    center_line = np.array(center_line[['x', 'y']])
    
    # Create a LineString from the center line points
    line_string = LineString(center_line)
    
    return line_string

def polygon_from_borders(right_borders, left_borders):
    if right_borders is None or left_borders is None:
        print("Right or left borders are None.")
        return None
    
    right_borders = np.array(right_borders)
    left_borders = np.array(left_borders)
    
    # Create a polygon from the borders
    points = np.vstack((right_borders, left_borders[::-1]))  # Reverse left borders to close the polygon
    polygon = Polygon(points)
    
    return polygon

def plot_track_with_polygon(right_borders, left_borders):
    if right_borders is None or left_borders is None:
        print("Right or left borders are None.")
        return
    
    right_borders = np.array(right_borders)
    left_borders = np.array(left_borders)
    
    plt.figure(figsize=(10, 10))
    plt.plot(right_borders[:, 0], right_borders[:, 1], label='Right Border', color='blue')
    plt.plot(left_borders[:, 0], left_borders[:, 1], label='Left Border', color='red')
    
    # Create and plot the polygon
    points = np.vstack((right_borders, left_borders[::-1]))
    polygon = Polygon(points)
    x, y = polygon.exterior.xy
    plt.fill(x, y, alpha=0.5, fc='green', ec='black', label='Track Area')
    
    plt.title('Track Borders with Polygon')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.axis('equal')
    plt.grid()
    plt.show()

def plot_track_with_linestring(center_line):
    if center_line is None or center_line.empty:
        print("Center line is empty or None.")
        return
    
    center_line = np.array(center_line[['x', 'y']])
    
    plt.figure(figsize=(10, 10))
    plt.plot(center_line[:, 0], center_line[:, 1], label='Center Line', color='black')
    plt.title('Track Center Line')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.axis('equal')
    plt.grid()
    plt.show()

df = import_circuit_from_csv("./simple_track.csv") # Import the track data
right_borders, left_borders = compute_borders(df) # Compute borders
plot_track_with_polygon(right_borders, left_borders) # Plot the track
plot_track_with_linestring(df) # Plot the center line
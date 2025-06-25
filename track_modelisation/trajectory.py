import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon
from scipy.interpolate import splprep, splev
from shapely.geometry import Point
from matplotlib.animation import FuncAnimation


class Trajectory:
    def __init__(self, points=None):
        self.points = np.array(points) 

    def plot_on_track(self, track):
        plt.figure(figsize=(10, 10))

        x, y = track.polygon.exterior.xy
        plt.plot(x, y, color='blue', label='Track Polygon')
        plt.fill(x, y, alpha=0.5, fc='blue', ec='black')

        plt.title('Trajectory on Track')
        self.points = track.smooth_line(self.points, smoothing = 10 , num_points=1000)
        x , y = self.points[:, 0], self.points[:, 1]
        plt.plot(x, y, color='red', label='Trajectory')
        plt.show()

    def animation_on_track(self,track):
        x , y = self.points[:, 0], self.points[:, 1]
        fig , axis = plt.subplots()
        axis.set_xlim([min(x) - 10, max(x) + 10])
        axis.set_ylim([min(y) -10, max(y) + 10])

        track_x, track_y = track.polygon.exterior.xy
        axis.plot(track_x, track_y, color='blue', label='Track Polygon')
        axis.fill(track_x, track_y, alpha=0.1, fc='blue', ec='black')

        animated_plot, = axis.plot([],[], color = 'red')
        print(animated_plot)
        
        def update_data(frame):
            animated_plot.set_data(x[:frame],y[:frame])
            return animated_plot

        animation = FuncAnimation(fig = fig,
                                  func = update_data,
                                  frames= len(x),
                                  interval = 100 ,
                                  )
        
        plt.show()

    




        






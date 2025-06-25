import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon
from scipy.interpolate import splprep, splev
from shapely.geometry import Point


class Car:
    def __init__(self, x=0.0, y=0.0, angle=0.0):
        self.position = np.array([x, y], dtype=float)
        self.angle = angle  # in radians

    def set_position(self, x, y):
        self.position = np.array([x, y], dtype=float)

    def set_angle(self, angle):
        self.angle = angle

    def move(self, distance):
        dx = distance * np.cos(self.angle)
        dy = distance * np.sin(self.angle)
        self.position += np.array([dx, dy])
    
    def closest_point_on_track(self, track):
        if track.centerline is None or len(track.centerline) == 0:
            raise ValueError("Track centerline is empty or None")

        closest_point = Point(self.position)
        distances = [closest_point.distance(Point(pt)) for pt in track.centerline]
        closest_index = np.argmin(distances)
        return track.centerline[closest_index]
    
    def go_to_closest_point(self, track):
        closest_point = self.closest_point_on_track(track)
        self.set_position(*closest_point)

    def move_along_the_centerline(self, track, distance):
        # Trouver le point suivant sur la centerline
        current_point = Point(self.position)
        centerline_points = track.centerline
        
        # Trouver l'index du point le plus proche
        distances = [current_point.distance(Point(pt)) for pt in centerline_points]
        current_index = np.argmin(distances)
        
        # Calculer le prochain index (en boucle)
        next_index = (current_index + 1) % len(centerline_points)
        next_point = centerline_points[next_index]
        
        # Calculer la direction vers le prochain point
        direction = np.array(next_point) - self.position
        direction_norm = np.linalg.norm(direction)
        
        if direction_norm > 0:
            # Normaliser la direction et multiplier par la distance
            direction = direction / direction_norm * distance
            self.position += direction

    def basic_mvmnt_along_the_centerline(self, track, distance):        
        x, y = track.polygon.exterior.xy
        plt.plot(x, y, color='blue', label='Track Polygon')
        plt.fill(x, y, alpha=0.5, fc='blue', ec='black')
        plt.title('Car Movement Along Track Centerline')    

        car_scatter = None  # Store the scatter plot object

        for _ in range(distance):
            self.move_along_the_centerline(track, distance=10)
            car_scatter = plt.scatter(self.position[0], self.position[1], color='orange', s=20, label='Car')
            plt.axis('equal')
            plt.legend()
            plt.pause(0.1)
            car_scatter.remove()

        plt.title('Car Movement Along Track Centerline')    
        plt.show()





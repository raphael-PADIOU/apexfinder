import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt


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

        # Find the closest point on the centerline to the car's current position
        closest_point = Point(self.position)
        distances = [closest_point.distance(Point(pt)) for pt in track.centerline]
        closest_index = np.argmin(distances)
        return track.centerline[closest_index]
    
    def go_to_closest_point(self, track):
        closest_point = self.closest_point_on_track(track)
        self.set_position(*closest_point)

    def move_along_the_centerline(self, track, distance):        
        centerline = track.centerline
        if centerline is None or len(centerline) == 0:
            raise ValueError("Track centerline is empty or None")

        # Find the closest point on the centerline to the car's current position
        closest_point = Point(self.position)
        distances = [closest_point.distance(Point(pt)) for pt in centerline]
        closest_index = np.argmin(distances)

        # Move along the centerline
        next_index = (closest_index + int(distance)) % len(centerline)
        self.set_position(*centerline[next_index])





import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon
from scipy.interpolate import splprep, splev
from shapely.geometry import Point


class Track:
    def __init__(self, centerline=None, borders=None, polygon=None):
        self.centerline = centerline  # DataFrame or np.array of centerline points
        self.borders = borders        # Tuple: (right_borders, left_borders)
        self.polygon = polygon        # Shapely Polygon

    @staticmethod
    def import_circuit_from_csv(filepath):
        try:
            df = pd.read_csv(filepath)
            return df  # returns a df with the center line of the track
        except Exception as e:
            print(f"Error importing circuit from {filepath}: {e}")
            return None

    @staticmethod
    def smooth_line(border_points, smoothing=5.0, num_points=500):
        border_points = np.array(border_points)
        x, y = border_points[:, 0], border_points[:, 1]
        tck, _ = splprep([x, y], s=smoothing, per=True)
        u_new = np.linspace(0, 1, num_points)
        x_new, y_new = splev(u_new, tck)
        return np.vstack((x_new, y_new)).T

    @staticmethod
    def linestring_from_array(line):
        if line is None or len(line) == 0:
            print("Line is empty or None.")
            return None
        if not np.allclose(line[0], line[-1]):
            line = np.vstack([line, line[0]])
        return LineString(line)

    @classmethod
    def from_csv(cls, filepath, width=15): # factory method to create a Track instance from a CSV file
        df = cls.import_circuit_from_csv(filepath)
        if df is None or df.empty:
            print("Failed to import or empty DataFrame.")
            return None
        centerline = np.array(df[['x', 'y']])
        right_borders, left_borders = cls.compute_borders(centerline, width)
        polygon = cls.track_from_borders(right_borders, left_borders)
        return cls(centerline=centerline, borders=(right_borders, left_borders), polygon=polygon)

    @staticmethod
    def compute_borders(center_line, width=15):
        if center_line is None or len(center_line) == 0:
            print("Center line is empty or None.")
            return None, None

        left_borders = []
        right_borders = []

        for i in range(len(center_line)):
            next_i = (i + 1) % len(center_line)
            dx = center_line[next_i][0] - center_line[i][0]
            dy = center_line[next_i][1] - center_line[i][1]
            length = np.sqrt(dx**2 + dy**2)
            if length == 0:
                continue
            nx = dy / length * (width / 2)
            ny = -dx / length * (width / 2)
            right_borders.append([center_line[i][0] + nx, center_line[i][1] + ny])
            left_borders.append([center_line[i][0] - nx, center_line[i][1] - ny])

        if not np.allclose(right_borders[0], right_borders[-1]):
            right_borders.append(right_borders[0])
        if not np.allclose(left_borders[0], left_borders[-1]):
            left_borders.append(left_borders[0])

        right_borders_smooth = Track.smooth_line(right_borders)
        left_borders_smooth = Track.smooth_line(left_borders[::-1])
        return right_borders_smooth, left_borders_smooth

    @staticmethod
    def track_from_borders(right_borders, left_borders):
        if right_borders is None or left_borders is None:
            print("Borders linestrings are empty or None.")
            return None
        polygon_coords = np.vstack((right_borders, left_borders))
        track_polygon = Polygon(polygon_coords)
        return track_polygon

    def plot(self):
        if self.polygon is None:
            print("Track polygon is empty or None.")
            return
        x, y = self.polygon.exterior.xy
        plt.figure(figsize=(10, 10))
        plt.title('Track Polygon')
        plt.plot(x, y, color='blue', label='Track Polygon')
        plt.fill(x, y, alpha=0.5, fc='blue', ec='black')
        plt.axis('equal')
        plt.show()

    def plot_with_car(self, car):
            if car is None or self.polygon is None:
                print("Car or track polygon is None.")
                return

            x, y = self.polygon.exterior.xy
            plt.plot(x, y, color='blue', label='Track Polygon')
            plt.fill(x, y, alpha=0.5, fc='blue', ec='black')
            plt.scatter(car.position[0], car.position[1], color='orange', s=20, label='Car')
            plt.axis('equal')
            plt.legend()
            plt.show()

    def greedy_optimized_trajectory(self):
        borders = self.borders
        


    


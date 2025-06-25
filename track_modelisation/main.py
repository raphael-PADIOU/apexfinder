import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon
from scipy.interpolate import splprep, splev
from shapely.geometry import Point

from car import Car
from track import Track


car = Car(x=10, y=5, angle=np.pi / 2)
track = Track.from_csv("simple_track.csv", width=15)

car.go_to_closest_point(track)

car.basic_mvmnt_along_the_centerline(track, distance=200)

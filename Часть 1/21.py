import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import random
import os

def generate_line(num_points, min_distance, max_distance):
    points = [np.random.uniform(-100, 100, 3)]
    for i in range(1, num_points):
        distance = np.random.uniform(min_distance, max_distance)
        direction = np.random.uniform(-1, 1, 3)
        direction /= np.linalg.norm(direction)
        new_point = points[-1] + direction * distance
        points.append(new_point)
    return points

def save_to_obj(points, filename):
    with open(filename, 'w') as f:
        for i, point in enumerate(points):
            f.write(f"v {point[0]} {point[1]} {point[2]}\n")
        for i in range(len(points) - 1):
            f.write(f"l {i+1} {i+2}\n")

num_points = 100
min_distance = 1
max_distance = 5

points = generate_line(num_points, min_distance, max_distance)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "line.obj")
save_to_obj(points, filename)
print(f"Model saved as {filename}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(*zip(*points), 'b-', linewidth=5)
plt.show()
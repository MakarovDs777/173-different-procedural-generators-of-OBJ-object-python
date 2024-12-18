import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import random
import os

def generate_line(num_points, min_distance, max_distance, radius, num_circles):
    points = [np.random.uniform(-100, 100, 3)]
    for i in range(1, num_points):
        distance = np.random.uniform(min_distance, max_distance)
        direction = np.random.uniform(-1, 1, 3)
        direction /= np.linalg.norm(direction)
        new_point = points[-1] + direction * distance
        points.append(new_point)

    # Создание трубки
    tube_points = []
    tube_faces = []
    for j in range(len(points) - 1):
        x1, y1, z1 = points[j]
        x2, y2, z2 = points[j+1]
        vec = np.array([x2-x1, y2-y1, z2-z1])
        vec = vec / np.linalg.norm(vec)
        perp_vec1 = np.array([vec[1], -vec[0], 0])
        perp_vec1 = perp_vec1 / np.linalg.norm(perp_vec1)
        perp_vec2 = np.cross(vec, perp_vec1)
        perp_vec2 = perp_vec2 / np.linalg.norm(perp_vec2)
        for k in range(num_circles):
            angle = 2 * np.pi * k / num_circles
            pos1 = np.array([x1, y1, z1]) + radius * (np.cos(angle) * perp_vec1 + np.sin(angle) * perp_vec2)
            pos2 = np.array([x2, y2, z2]) + radius * (np.cos(angle) * perp_vec1 + np.sin(angle) * perp_vec2)
            tube_points.append(pos1.tolist())
            tube_points.append(pos2.tolist())
            tube_faces.append([len(tube_points)-2, len(tube_points)-1, len(tube_points)])
            tube_faces.append([len(tube_points)-1, len(tube_points)-2, len(tube_points)])

    return tube_points, tube_faces

def save_to_obj(points, faces, filename):
    with open(filename, 'w') as f:
        for i, point in enumerate(points):
            f.write(f"v {point[0]} {point[1]} {point[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

num_points = 100
min_distance = 1
max_distance = 5
radius = 5
num_circles = 10

points, faces = generate_line(num_points, min_distance, max_distance, radius, num_circles)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "tube.obj")
save_to_obj(points, faces, filename)
print(f"Model saved as {filename}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(*zip(*points), 'b-', linewidth=5)
plt.show()
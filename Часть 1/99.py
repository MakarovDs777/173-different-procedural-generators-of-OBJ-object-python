import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def generate_corridor_field(shape, num_points=10):
    points = []
    for _ in range(num_points):
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        z = shape[2] // 2
        points.append([x, y, z])

    meshes = []
    for i in range(len(points) - 1):
        start_point = points[i]
        end_point = points[i + 1]
        start_x, start_y, start_z = start_point
        end_x, end_y, end_z = end_point

        length = max(abs(end_x - start_x), abs(end_y - start_y))
        if length == 0:
            continue

        for j in range(length + 1):
            new_x = start_x + j * (end_x - start_x) // length
            new_y = start_y + j * (end_y - start_y) // length
            new_z = start_z
            size = 2
            box = trimesh.primitives.Box(extents=(size, size, size), transform=trimesh.transformations.translation_matrix([new_x, new_y, new_z]))
            meshes.append(box)

    mesh = trimesh.util.concatenate(meshes)
    return mesh

shape = (128, 128, 128)
corridor_field = generate_corridor_field(shape)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "corridor.obj")
corridor_field.export(filename)
print(f"Model saved as {filename}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(corridor_field.vertices[:, 0], corridor_field.vertices[:, 1], corridor_field.vertices[:, 2], color='r', alpha=0.5)
for face in corridor_field.faces:
    v1, v2, v3 = corridor_field.vertices[face]
    ax.plot3D([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], 'r', alpha=0.5)
    ax.plot3D([v2[0], v3[0]], [v2[1], v3[1]], [v2[2], v3[2]], 'r', alpha=0.5)
    ax.plot3D([v3[0], v1[0]], [v3[1], v1[1]], [v3[2], v1[2]], 'r', alpha=0.5)
plt.show()

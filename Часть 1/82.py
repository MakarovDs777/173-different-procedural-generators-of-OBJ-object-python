import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def generate_cube_field(shape):
    points = []
    for _ in range(10):
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        points.append([x, y, shape[2] // 2])

    meshes = []
    for point in points:
        x, y, z = point
        size = np.random.randint(4, 8)
        box = trimesh.primitives.Box(extents=(size, size, size), transform=trimesh.transformations.translation_matrix([x, y, z]))
        meshes.append(box)

    for i in range(len(points) - 1):
        dx = points[i+1][0] - points[i][0]
        dy = points[i+1][1] - points[i][1]
        dz = 0
        length = int(np.sqrt(dx**2 + dy**2))
        for j in range(length):
            new_x = int(points[i][0] + j * dx // length)
            new_y = int(points[i][1] + j * dy // length)
            new_z = int(points[i][2])
            size = 2
            box = trimesh.primitives.Box(extents=(size, size, size), transform=trimesh.transformations.translation_matrix([new_x, new_y, new_z]))
            meshes.append(box)

    mesh = trimesh.util.concatenate(meshes)
    return mesh

def wrap_mesh_in_convex_hull(mesh):
    hull = trimesh.convex.convex_hull(mesh.vertices)
    return hull

shape = (128, 128, 128)
cube_field = generate_cube_field(shape)

# Обернуть структуру в меш с вершинами и гранями
wrapped_mesh = wrap_mesh_in_convex_hull(cube_field)

# Удалить исходную структуру
del cube_field

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "cube.obj")
wrapped_mesh.export(filename)
print(f"Model saved as {filename}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(wrapped_mesh.vertices[:, 0], wrapped_mesh.vertices[:, 1], wrapped_mesh.vertices[:, 2], color='r', alpha=0.5)
for face in wrapped_mesh.faces:
    v1, v2, v3 = wrapped_mesh.vertices[face]
    ax.plot3D([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], 'r', alpha=0.5)
    ax.plot3D([v2[0], v3[0]], [v2[1], v3[1]], [v2[2], v3[2]], 'r', alpha=0.5)
    ax.plot3D([v3[0], v1[0]], [v3[1], v1[1]], [v3[2], v1[2]], 'r', alpha=0.5)
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import trimesh
import os

def generate_delaunay_field(shape):
    array = np.zeros(shape, dtype=float)

    points2 = []
    for _ in range(50):  
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        z = 2 * shape[2] // 3  
        points2.append([x, y, z])

    for i in range(len(points2) - 1):
        start_point = points2[i]
        end_point = points2[i + 1]

        for new_x in range(min(start_point[0], end_point[0]), max(start_point[0], end_point[0]) + 1):
            new_y = start_point[1]
            new_z = start_point[2]

            for height_offset in range(-1, 5):  
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
                    array[new_x, new_y, new_z + height_offset] = 1.0

    return array

shape = (128, 128, 128)  

delaunay_field = generate_delaunay_field(shape)

# Generate a mesh from your array
verts, faces, _, _ = measure.marching_cubes(delaunay_field, level=0.5)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "delaunay.obj")
with open(filename, "w") as f:
    for vert in verts:
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], color='r', alpha=0.5)
plt.show()

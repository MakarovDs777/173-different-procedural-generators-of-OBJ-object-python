import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_tube_field(shape, num_tubes, distance, outer_radius, inner_radius):
    array = np.zeros(shape, dtype=float)

    for i in range(num_tubes):
        # Определяем центр трубы
        x_center = (i % 8) * distance + distance // 2
        y_center = ((i // 8) % 8) * distance + distance // 2
        z_center = shape[2] // 2

        # Создание трубы
        for z in range(shape[2]):
            for angle in np.linspace(0, 2 * np.pi, 30):
                outer_x = int(x_center + outer_radius * np.cos(angle))
                outer_y = int(y_center + outer_radius * np.sin(angle))
                inner_x = int(x_center + inner_radius * np.cos(angle))
                inner_y = int(y_center + inner_radius * np.sin(angle))

                # Заполнение внешней части трубы
                if 0 <= outer_x < shape[0] and 0 <= outer_y < shape[1]:
                    array[outer_x, outer_y, z] = 1.0

                # Убираем внутреннюю часть
                if 0 <= inner_x < shape[0] and 0 <= inner_y < shape[1]:
                    array[inner_x, inner_y, z] = 0.0

    return array

shape = (64, 64, 64)
num_tubes = 100
distance = 10
outer_radius = 3  # Внешний радиус трубы
inner_radius = 2  # Внутренний радиус трубы

tube_field = generate_tube_field(shape, num_tubes, distance, outer_radius, inner_radius)

verts, faces, _, _ = measure.marching_cubes(tube_field, level=0.5)

# Удаляем внутренние грани из результата
verts = verts[verts[:, 2] > 0]
faces = faces[np.all(faces < len(verts), axis=1)]

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "tubes.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Сохранено как {filename}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], color='blue', alpha=0.5)
plt.show()
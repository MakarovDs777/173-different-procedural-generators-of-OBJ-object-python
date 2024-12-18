import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_tube_field(shape, num_tubes, tube_length, tube_radius):
    array = np.zeros(shape, dtype=float)
    x_positions = np.linspace(0, shape[0] - tube_radius, num_tubes // 2)
    y_positions = np.linspace(0, shape[1] - tube_radius, num_tubes // 2)
    z_position = shape[2] // 2
    for i in range(num_tubes // 2):
        for j in range(num_tubes // 2):
            x = x_positions[i]
            y = y_positions[j]
            for z in range(shape[2]):
                if 0 <= x < shape[0] and 0 <= y < shape[1] and 0 <= z < shape[2]:
                    # Создайте двумерную гауссову функцию для круглого поперечного сечения
                    xx, yy = np.meshgrid(np.arange(shape[0]) - x, np.arange(shape[1]) - y)
                    gaussian = (1 / (2 * np.pi * tube_radius ** 2)) * np.exp(-(xx ** 2 + yy ** 2) / (2 * tube_radius ** 2))
                    array[z, :, :] += gaussian
            # Добавить трубы в другом направлении
            x = y_positions[i]
            y = x_positions[j]
            for z in range(shape[2]):
                if 0 <= x < shape[0] and 0 <= y < shape[1] and 0 <= z < shape[2]:
                    # Создайте двумерную гауссову функцию для круглого поперечного сечения
                    xx, yy = np.meshgrid(np.arange(shape[0]) - x, np.arange(shape[1]) - y)
                    gaussian = (1 / (2 * np.pi * tube_radius ** 2)) * np.exp(-(xx ** 2 + yy ** 2) / (2 * tube_radius ** 2))
                    array[z, :, :] += gaussian
    return array

# Параметры
shape = (64, 64, 64)
num_tubes = 10
tube_length = 64
tube_radius = 3

# Создайте трехмерное поле с помощью круглых труб
tube_field = generate_tube_field(shape, num_tubes, tube_length, tube_radius)

# Создание изоповерхности из трехмерного поля
verts, faces, _, _ = measure.marching_cubes(tube_field, level=0.5 * np.max(tube_field))

# Сохраните изурфейса в OBJ-файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "round_tube.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]:.4f} {vert[1]:.4f} {vert[2]:.4f}\n")
    for face in faces:
        f.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)
plt.show()
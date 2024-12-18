import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_tube_field(shape, num_tubes, tube_length, tube_radius):
    array = np.zeros(shape, dtype=float)
    for _ in range(num_tubes):
        x, y = np.random.randint(0, shape[0]), np.random.randint(0, shape[1])
        z = 0
        for _ in range(tube_length):
            if 0 <= x < shape[0] and 0 <= y < shape[1] and 0 <= z < shape[2]:
                for i in range(-tube_radius, tube_radius + 1):
                    for j in range(-tube_radius, tube_radius + 1):
                        if i ** 2 + j ** 2 <= tube_radius ** 2:
                            xi = np.clip(x + i, 0, shape[0] - 1)
                            yi = np.clip(y + j, 0, shape[1] - 1)
                            array[xi, yi, z] = 1.0
            z += 1
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
num_tubes = 10  # Количество труб
tube_length = 64  # Длина труб
tube_radius = 3  # Радиус труб

# Генерация 3D-поля с трубами
tube_field = generate_tube_field(shape, num_tubes, tube_length, tube_radius)

# Создание изосурфейса из 3D-поля
verts, faces, _, _ = measure.marching_cubes(tube_field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "tube.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)
plt.show()
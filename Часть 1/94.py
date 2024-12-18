import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from scipy.spatial import Delaunay
import os

# Функция для генерации 3D-поля с коридорами
def generate_corridors_field(shape):
    array = np.zeros(shape, dtype=float)

    # Генерация коридоров между точками
    points = []
    for level in range(3):
        for _ in range(10):
            x = np.random.randint(10, shape[0] - 10)
            y = np.random.randint(10, shape[1] - 10)
            z = level * (shape[2] // 3) + np.random.randint(10, shape[2] // 3 - 10)
            points.append([x, y, z])

    # Генерация коридоров между точками
    for i in range(len(points) - 1):
        dx = points[i+1][0] - points[i][0]
        dy = points[i+1][1] - points[i][1]
        dz = points[i+1][2] - points[i][2]
        length_x = abs(dx)
        length_y = abs(dy)
        length_z = abs(dz)
        max_length = max(length_x, length_y, length_z)
        for j in range(max_length):
            if j < length_x:
                new_x = int(points[i][0] + j * dx // length_x)
            else:
                new_x = points[i+1][0]
            if j < length_y:
                new_y = int(points[i][1] + j * dy // length_y)
            else:
                new_y = points[i+1][1]
            if j < length_z:
                new_z = int(points[i][2] + j * dz // length_z)
            else:
                new_z = points[i+1][2]
            if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                array[new_x, new_y, new_z] = 1.0
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        for m in range(-2, 3):
                            x1, y1, z1 = new_x + k, new_y + l, new_z + m
                            if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                array[x1, y1, z1] = 1.0

    return array

# Параметры
shape = (128, 128, 128)  # Размеры 3D массива

# Генерация 3D-поля с коридорами
corridors_field = generate_corridors_field(shape)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(corridors_field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "corridors.obj")
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
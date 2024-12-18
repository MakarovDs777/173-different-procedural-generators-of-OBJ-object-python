import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from scipy.spatial import Delaunay
import os

# Функция для генерации 3D-поля с триангуляцией Делоне
def generate_delaunay_field(shape, num_cubes, distance):
    array = np.zeros(shape, dtype=float)

    # Генерация сетки коридоров
    for x in range(0, shape[0], distance):
        for y in range(0, shape[1], distance):
            for z in range(0, shape[2], distance):
                # Генерация коридора по оси X
                for i in range(distance):
                    new_x = x + i
                    new_y = y
                    new_z = z
                    if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                        array[new_x, new_y, new_z] = 1.0
                # Генерация коридора по оси Y
                for i in range(distance):
                    new_x = x
                    new_y = y + i
                    new_z = z
                    if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                        array[new_x, new_y, new_z] = 1.0
                # Генерация коридора по оси Z
                for i in range(distance):
                    new_x = x
                    new_y = y
                    new_z = z + i
                    if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                        array[new_x, new_y, new_z] = 1.0

    # Генерация комнат в стыке коридоров
    for x in range(0, shape[0], distance):
        for y in range(0, shape[1], distance):
            for z in range(0, shape[2], distance):
                # Генерация комнаты
                generate_cube(array, (x, y, z), 5)

    return array

# Функция для генерации куба в заданной точке
def generate_cube(array, point, size):
    x, y, z = int(point[0]), int(point[1]), int(point[2])
    for i in range(-size, size+1):
        for j in range(-size, size+1):
            for k in range(-size, size+1):
                new_x, new_y, new_z = x + i, y + j, z + k
                if 0 <= new_x < array.shape[0] and 0 <= new_y < array.shape[1] and 0 <= new_z < array.shape[2]:
                    array[new_x, new_y, new_z] = 1.0

# Параметры
shape = (128, 128, 128)  # Размеры 3D массива
num_cubes = 60
distance = 10  # Расстояние между кубами

# Генерация 3D-поля с триангуляцией Делоне
delaunay_field = generate_delaunay_field(shape, num_cubes, distance)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(delaunay_field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "delaunay.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], color='blue', alpha=0.5)
plt.show()

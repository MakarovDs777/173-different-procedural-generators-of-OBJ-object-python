import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os
# Генерация случайной функции с двумя переменными
def generate_function():
    functions = [lambda x, y: x + y, lambda x, y: x - y, lambda x, y: x * y, lambda x, y: x / y]
    return random.choice(functions)

# Генерация фрактала
def generate_fractal(x, y, z, depth):
    if depth == 0:
        return np.array([x, y, z])
    else:
        x1 = x + np.random.uniform(-1, 1)
        y1 = y + np.random.uniform(-1, 1)
        z1 = z + np.random.uniform(-1, 1)
        return np.array([x1, y1, z1]) + generate_fractal(x1, y1, z1, depth - 1)

# Генерация полостей и самоподобия
def generate_cavity(x, y, z, depth):
    if depth == 0:
        return np.array([x, y, z])
    else:
        x1 = x + np.random.uniform(-1, 1)
        y1 = y + np.random.uniform(-1, 1)
        z1 = z + np.random.uniform(-1, 1)
        return np.array([x1, y1, z1]) + generate_cavity(x1, y1, z1, depth - 1)

# Генерация трехмерного пространства
def generate_space():
    x = np.random.uniform(-10, 10)
    y = np.random.uniform(-10, 10)
    z = np.random.uniform(-10, 10)
    depth = np.random.randint(1, 10)
    return generate_fractal(x, y, z, depth)

# Генерация линии
def generate_line():
    points = []
    for i in range(100):
        x, y, z = generate_space()
        points.append([x, y, z])
    return points

# Генерация 3D-поля с линией
def generate_line_field(shape, line):
    array = np.zeros(shape, dtype=float)
    for point in line:
        x, y, z = int(point[0] / 20 + shape[0] / 2), int(point[1] / 20 + shape[1] / 2), int(point[2] / 20 + shape[2] / 2)
        if 0 <= x < shape[0] and 0 <= y < shape[1] and 0 <= z < shape[2]:
            array[x, y, z] = 1.0
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива

# Генерация линии
line = generate_line()

# Генерация 3D-поля с линией
line_field = generate_line_field(shape, line)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(line_field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "line.obj")
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

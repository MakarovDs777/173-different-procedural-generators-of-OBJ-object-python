import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy.interpolate import make_interp_spline
from skimage import measure
import os

# Функция для генерации случайной точки в 3D пространстве
def generate_point():
    x = np.random.uniform(-10, 10)
    y = np.random.uniform(-10, 10)
    z = np.random.uniform(-10, 10)
    return np.array([x, y, z])

# Функция для генерации фрактала
def generate_fractal(point, depth):
    if depth == 0:
        return point
    else:
        x = point[0] + np.random.uniform(-1, 1)
        y = point[1] + np.random.uniform(-1, 1)
        z = point[2] + np.random.uniform(-1, 1)
        return generate_fractal(np.array([x, y, z]), depth - 1)

# Функция для генерации полостей и самоподобия
def generate_cavity(point, depth):
    if depth == 0:
        return point
    else:
        x = point[0] + np.random.uniform(-1, 1)
        y = point[1] + np.random.uniform(-1, 1)
        z = point[2] + np.random.uniform(-1, 1)
        return generate_cavity(np.array([x, y, z]), depth - 1)

# Функция для генерации 3D пространства
def generate_space(depth):
    point = generate_point()
    return generate_fractal(point, depth) + generate_cavity(point, depth)

# Функция для сохранения файла OBJ
def save_obj_file(verts, faces, filename):
    with open(filename, "w") as f:
        for j, vert in enumerate(verts):
            f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

# Параметры
num_points = 100
depth = 5

# Генерация точек в 3D пространстве
points = [generate_space(depth) for _ in range(num_points)]

# Интерполяция сплайном
t = np.linspace(0, 1, num_points)
x = np.array([point[0] for point in points])
y = np.array([point[1] for point in points])
z = np.array([point[2] for point in points])

t_interp = np.linspace(0, 1, 1000)
x_interp = make_interp_spline(t, x, k=3)(t_interp)
y_interp = make_interp_spline(t, y, k=3)(t_interp)
z_interp = make_interp_spline(t, z, k=3)(t_interp)

# Создание 3D массива из массива вершин
verts = np.column_stack((x_interp, y_interp, z_interp))
volume = np.zeros((10, 10, 10), dtype=bool)
volume[np.clip(np.round(verts[:, 0]), 0, 9).astype(np.int_), np.clip(np.round(verts[:, 1]), 0, 9).astype(np.int_), np.clip(np.round(verts[:, 2]), 0, 9).astype(np.int_)] = True

# Создание изосурфейса
faces = measure.marching_cubes(volume, level=0.5)[0]

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "output.obj")
save_obj_file(verts, faces, filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)
plt.show()
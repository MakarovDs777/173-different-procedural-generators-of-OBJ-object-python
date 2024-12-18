import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from scipy.interpolate import interp1d
import os
import random
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

# Визуализация пространства
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

points = []
for i in range(100):
    x, y, z = generate_space()
    points.append([x, y, z])

# Интерполяция
t = np.linspace(0, 1, len(points))
x = np.array([point[0] for point in points])
y = np.array([point[1] for point in points])
z = np.array([point[2] for point in points])

x_interp = interp1d(t, x, kind='cubic')
y_interp = interp1d(t, y, kind='cubic')
z_interp = interp1d(t, z, kind='cubic')

t_interp = np.linspace(0, 1, 1000)
x_interp = x_interp(t_interp)
y_interp = y_interp(t_interp)
z_interp = z_interp(t_interp)

ax.plot(x_interp, y_interp, z_interp, 'b-')

ax.scatter(*zip(*points))

# Создание 3D массива для генерации изосурфейса
shape = (64, 64, 64)
array = np.zeros(shape, dtype=float)

for i in range(len(points) - 1):
    dx = points[i+1][0] - points[i][0]
    dy = points[i+1][1] - points[i][1]
    dz = points[i+1][2] - points[i][2]
    length = int(np.sqrt(dx**2 + dy**2 + dz**2))
    for j in range(length):
        new_x = int(points[i][0] + j * dx // length)
        new_y = int(points[i][1] + j * dy // length)
        new_z = int(points[i][2] + j * dz // length)
        if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
            array[new_x, new_y, new_z] = 1.0
            # Делаем линии более жирными
            if new_x > 0:
                array[new_x-1, new_y, new_z] = 1.0
            if new_x < shape[0] - 1:
                array[new_x+1, new_y, new_z] = 1.0
            if new_y > 0:
                array[new_x, new_y-1, new_z] = 1.0
            if new_y < shape[1] - 1:
                array[new_x, new_y+1, new_z] = 1.0
            if new_z > 0:
                array[new_x, new_y, new_z-1] = 1.0
            if new_z < shape[2] - 1:
                array[new_x, new_y, new_z+1] = 1.0

# Генерация изосурфейса
verts, faces, _, _ = measure.marching_cubes(array, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "lines.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")


# Визуализация вершин и граней изосурфейса
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Визуализация вершин
ax.scatter(verts[:, 0], verts[:, 1], verts[:, 2], c='b')

# Визуализация граней
for face in faces:
    ax.plot3D([verts[face[0], 0], verts[face[1], 0], verts[face[2], 0], verts[face[0], 0]],
              [verts[face[0], 1], verts[face[1], 1], verts[face[2], 1], verts[face[0], 1]],
              [verts[face[0], 2], verts[face[1], 2], verts[face[2], 2], verts[face[0], 2]], c='r')

plt.show()

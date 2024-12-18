import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy.interpolate import interp1d

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

# Генерация трубы
radius = 1.0
theta = np.linspace(0, 2*np.pi, 100)

tube_x = []
tube_y = []
tube_z = []

for i in range(len(x_interp)):
    for j in range(len(theta)):
        tube_x.append(x_interp[i] + radius * np.cos(theta[j]))
        tube_y.append(y_interp[i] + radius * np.sin(theta[j]))
        tube_z.append(z_interp[i])

# Создание вершин и треугольников для меша
vertices = []
faces = []

for i in range(len(x_interp) - 1):
    for j in range(len(theta)):
        idx1 = i * len(theta) + j
        idx2 = (i + 1) * len(theta) + j
        idx3 = (i + 1) * len(theta) + (j + 1) % len(theta)
        idx4 = i * len(theta) + (j + 1) % len(theta)

        vertices.append([tube_x[idx1], tube_y[idx1], tube_z[idx1]])
        vertices.append([tube_x[idx2], tube_y[idx2], tube_z[idx2]])
        vertices.append([tube_x[idx3], tube_y[idx3], tube_z[idx3]])
        vertices.append([tube_x[idx4], tube_y[idx4], tube_z[idx4]])

        faces.append([idx1, idx2, idx3])
        faces.append([idx1, idx3, idx4])

# Сохранение меша в файл
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "tube.obj")
with open(filename, "w") as f:
    for i, vertex in enumerate(vertices):
        f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
    for face in faces:
        f.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")
print(f"Tube saved as {filename}")

# Визуализация меша
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

mesh = Poly3DCollection(vertices, facecolors='b', alpha=0.5)
ax.add_collection3d(mesh)

plt.show()
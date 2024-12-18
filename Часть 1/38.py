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

# Сохранение изогнутой линии изурфейсом
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "curve.obj")
with open(filename, "w") as f:
    for i in range(len(x_interp)):
        f.write(f"v {x_interp[i]} {y_interp[i]} {z_interp[i]}\n")
    for i in range(len(x_interp) - 1):
        f.write(f"l {i+1} {i+2}\n")
print(f"Curve saved as {filename}")

plt.show()
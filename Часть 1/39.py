import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import os
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

ax.scatter(tube_x, tube_y, tube_z, s=0.1)

# Сохранение изогнутой линии изурфейсом
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "tube.obj")
with open(filename, "w") as f:
    for i in range(len(tube_x)):
        f.write(f"v {tube_x[i]} {tube_y[i]} {tube_z[i]}\n")
    for i in range(len(tube_x) - 1):
        f.write(f"l {i+1} {i+2}\n")
print(f"Tube saved as {filename}")

plt.show()
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

# Генерация поверхности
def generate_surface(xmin, xmax, ymin, ymax, nx, ny):
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    x, y = np.meshgrid(x, y)
    z = np.zeros((ny, nx))  # создаем плоскую поверхность
    return x, y, z

# Создание дырок
def create_holes(x, y, z, max_radius, max_depth):
    holes = []
    for i in range(10):  # генерируем 10 дырок
        x_hole = random.uniform(x.min(), x.max())
        y_hole = random.uniform(y.min(), y.max())
        radius = random.uniform(0.1, max_radius)
        depth = random.uniform(0, max_depth)
        for i in range(int(x.shape[0])):
            for j in range(int(x.shape[1])):
                if abs(x[i, j] - x_hole) <= radius and abs(y[i, j] - y_hole) <= radius:
                    z[i, j] = -depth
        holes.append((x_hole, y_hole, radius, depth))
    return x, y, z, holes

# Визуализация поверхности
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y, z = generate_surface(-10, 10, -10, 10, 100, 100)
x, y, z, holes = create_holes(x, y, z, 5, 5)

ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5)

# Визуализация дырок
for hole in holes:
    x_hole, y_hole, radius, depth = hole
    ax.plot_surface(x, y, np.full((y.shape[0], x.shape[1]), -depth), color='r', alpha=0.5)

# Сохранение файла в OBJ
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "surface_with_holes.obj")
with open(filename, "w") as f:
    for i in range(len(x)):
        for j in range(len(y)):
            if z[i, j] < 0:
                f.write(f"v {x[i, j]} {y[i, j]} {z[i, j]}\n")
            else:
                f.write(f"v {x[i, j]} {y[i, j]} {z[i, j]}\n")
    for i in range(len(x) - 1):
        for j in range(len(y) - 1):
            if z[i, j] < 0 and z[i + 1, j] < 0 and z[i, j + 1] < 0 and z[i + 1, j + 1] < 0:
                f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 1} {(i + 1) * len(y) + j + 2}\n")
                f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 2} {i * len(y) + j + 2}\n")
            elif z[i, j] >= 0 and z[i + 1, j] >= 0 and z[i, j + 1] >= 0 and z[i + 1, j + 1] >= 0:
                f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 1} {(i + 1) * len(y) + j + 2}\n")
                f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 2} {i * len(y) + j + 2}\n")
            elif z[i, j] < 0 and z[i + 1, j] >= 0 and z[i, j + 1] >= 0 and z[i + 1, j + 1] >= 0:
                f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 1} {(i + 1) * len(y) + j + 2}\n")
                f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 2} {i * len(y) + j + 2}\n")
            elif z[i, j] >= 0 and z[i + 1, j] < 0 and z[i, j + 1] < 0 and z[i + 1, j + 1] < 0:
                f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 1} {(i + 1) * len(y) + j + 2}\n")
                f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 2} {i * len(y) + j + 2}\n")
    print(f"Файл сохранен как {filename}")

plt.show()
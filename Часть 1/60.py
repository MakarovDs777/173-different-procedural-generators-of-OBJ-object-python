import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

# Генерация поверхности
def generate_surface(xmin, xmax, ymin, ymax, zmin, zmax, nx, ny):
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    x, y = np.meshgrid(x, y)
    z = np.random.uniform(zmin, zmax, size=(ny, nx))
    return x, y, z

# Генерация волос
def generate_hair(x, y, z, length, thickness):
    hair_x = []
    hair_y = []
    hair_z = []
    for i in range(len(x)):
        for j in range(len(y)):
            if np.random.uniform(0, 1) < 0.1:  # вероятность появления волоса
                hair_x.append(x[i, j])
                hair_y.append(y[i, j])
                hair_z.append(z[i, j] + np.random.uniform(0, length))
                for k in range(int(length / thickness)):
                    hair_x.append(x[i, j])
                    hair_y.append(y[i, j])
                    hair_z.append(z[i, j] + (k + 1) * thickness)
    return hair_x, hair_y, hair_z

# Генерация труб
def generate_tube(x, y, z, radius, length):
    tube_x = []
    tube_y = []
    tube_z = []
    theta = np.linspace(0, 2*np.pi, 100)
    for i in range(5):  # генерируем 5 труб
        for k in range(int(length / 0.1)):
            for l in range(len(theta)):
                tube_x.append(x[50, 50] + radius * np.cos(theta[l]))
                tube_y.append(y[50, 50] + radius * np.sin(theta[l]))
                tube_z.append(z[50, 50] + k * 0.1)
    return tube_x, tube_y, tube_z

# Создание меша для труб
def create_mesh(tube_x, tube_y, tube_z):
    vertices = []
    faces = []
    theta = np.linspace(0, 2*np.pi, 100)
    for i in range(len(tube_x) // len(theta) - 1):
        for j in range(len(theta) - 1):
            idx1 = i * len(theta) + j
            idx2 = (i + 1) * len(theta) + j
            idx3 = (i + 1) * len(theta) + (j + 1)
            idx4 = i * len(theta) + (j + 1)
            vertices.append([[tube_x[idx1], tube_y[idx1], tube_z[idx1]],
                            [tube_x[idx2], tube_y[idx2], tube_z[idx2]],
                            [tube_x[idx3], tube_y[idx3], tube_z[idx3]]])
            vertices.append([[tube_x[idx1], tube_y[idx1], tube_z[idx1]],
                            [tube_x[idx3], tube_y[idx3], tube_z[idx3]],
                            [tube_x[idx4], tube_y[idx4], tube_z[idx4]]])
    return vertices, faces

# Визуализация поверхности и волос
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y, z = generate_surface(-10, 10, -10, 10, 0, 1, 100, 100)
tube_x, tube_y, tube_z = generate_tube(x, y, z, 0.1, 5)
vertices, faces = create_mesh(tube_x, tube_y, tube_z)

ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
mesh = Poly3DCollection(vertices, facecolors='b', alpha=0.5)
ax.add_collection3d(mesh)

# Сохранение файла в OBJ
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "surface_with_tube.obj")
with open(filename, "w") as f:
    for i in range(len(x)):
        for j in range(len(y)):
            f.write(f"v {x[i, j]} {y[i, j]} {z[i, j]}\n")
    for i in range(len(vertices)):
        f.write(f"v {vertices[i][0]} {vertices[i][1]} {vertices[i][2]}\n")
    for i in range(len(x) - 1):
        for j in range(len(y) - 1):
            f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 1} {(i + 1) * len(y) + j + 2}\n")
            f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 2} {i * len(y) + j + 2}\n")
    for i in range(len(faces)):
        f.write(f"f {faces[i][0] + 1 + len(x) * len(y)} {faces[i][1] + 1 + len(x) * len(y)} {faces[i][2] + 1 + len(x) * len(y)}\n")
print(f"Файл сохранен как {filename}")

plt.show()
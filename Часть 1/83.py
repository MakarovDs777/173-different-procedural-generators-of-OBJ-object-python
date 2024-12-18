import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Генерация поверхности
def generate_surface(xmin, xmax, ymin, ymax, nx, ny):
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    x, y = np.meshgrid(x, y)
    z = np.zeros((ny, nx))  # создаем плоскую поверхность
    return x, y, z

# Визуализация поверхности
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y, z = generate_surface(-10, 10, -10, 10, 100, 100)

# Вытягиваем плоскость в куб
height = 5
z_cube = np.zeros((z.shape[0], z.shape[1], height))

for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        for k in range(height):
            z_cube[i, j, k] = k

# Визуализируем куб
for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        ax.plot([x[i, j], x[i, j]], [y[i, j], y[i, j]], [z_cube[i, j, 0], z_cube[i, j, -1]], color='b')

for i in range(z.shape[0]):
    for k in range(height):
        ax.plot([x[i, 0], x[i, -1]], [y[i, 0], y[i, -1]], [z_cube[i, 0, k], z_cube[i, -1, k]], color='b')

for j in range(z.shape[1]):
    for k in range(height):
        ax.plot([x[0, j], x[-1, j]], [y[0, j], y[-1, j]], [z_cube[0, j, k], z_cube[-1, j, k]], color='b')

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-1, height)

# Сохраняем в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "cube.obj")
with open(filename, "w") as f:
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            for k in range(height):
                f.write(f"v {x[i, j]} {y[i, j]} {z_cube[i, j, k]}\n")
    for i in range(z.shape[0] - 1):
        for j in range(z.shape[1] - 1):
            for k in range(height - 1):
                f.write(f"f {(i * z.shape[1] * height) + (j * height) + k + 1} {(i * z.shape[1] * height) + ((j + 1) * height) + k + 1} {(i * z.shape[1] * height) + ((j + 1) * height) + (k + 1) + 1}\n")
                f.write(f"f {(i * z.shape[1] * height) + (j * height) + k + 1} {(i * z.shape[1] * height) + ((j + 1) * height) + (k + 1) + 1} {(i * z.shape[1] * height) + (j * height) + (k + 1) + 1}\n")
                f.write(f"f {(i * z.shape[1] * height) + (j * height) + k + 1} {((i + 1) * z.shape[1] * height) + (j * height) + k + 1} {((i + 1) * z.shape[1] * height) + (j * height) + (k + 1) + 1}\n")
                f.write(f"f {(i * z.shape[1] * height) + (j * height) + k + 1} {((i + 1) * z.shape[1] * height) + (j * height) + (k + 1) + 1} {(i * z.shape[1] * height) + (j * height) + (k + 1) + 1}\n")
                f.write(f"f {((i + 1) * z.shape[1] * height) + (j * height) + k + 1} {((i + 1) * z.shape[1] * height) + ((j + 1) * height) + k + 1} {((i + 1) * z.shape[1] * height) + ((j + 1) * height) + (k + 1) + 1}\n")
                f.write(f"f {((i + 1) * z.shape[1] * height) + (j * height) + k + 1} {((i + 1) * z.shape[1] * height) + ((j + 1) * height) + (k + 1) + 1} {((i + 1) * z.shape[1] * height) + (j * height) + (k + 1) + 1}\n")

plt.show()
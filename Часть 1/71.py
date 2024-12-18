import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5)

# Сохранение файла в OBJ
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "surface.obj")
with open(filename, "w") as f:
    for i in range(len(x)):
        for j in range(len(y)):
            f.write(f"v {x[i, j]} {y[i, j]} {z[i, j]}\n")
    for i in range(len(x) - 1):
        for j in range(len(y) - 1):
            f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 1} {(i + 1) * len(y) + j + 2}\n")
            f.write(f"f {i * len(y) + j + 1} {(i + 1) * len(y) + j + 2} {i * len(y) + j + 2}\n")
print(f"Файл сохранен как {filename}")

plt.show()
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy import ndimage
import os

# Сгенерировать поверхность (в данном случае куб)
def generate_cube(xmin, xmax, ymin, ymax, zmin, zmax, nx, ny, nz):
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    z = np.linspace(zmin, zmax, nz)
    x, y, z = np.meshgrid(x, y, z)
    return x, y, z

# Создать отверстия
def create_holes(x, y, z, max_radius, max_depth):
    holes = []
    for i in range(10):  # Создайте 10 отверстий
        x_hole = random.uniform(x.min(), x.max())
        y_hole = random.uniform(y.min(), y.max())
        z_hole = random.uniform(z.min(), z.max())
        radius = random.uniform(0.1, max_radius)
        depth = random.uniform(0, max_depth)

        # Создайте сферическое отверстие с заданным радиусом и глубиной
        x_hole_grid, y_hole_grid, z_hole_grid = np.meshgrid(
            np.linspace(x_hole - radius, x_hole + radius, 100),
            np.linspace(y_hole - radius, y_hole + radius, 100),
            np.linspace(z_hole - radius, z_hole + radius, 100)
        )
        mask = (x_hole_grid**2 + y_hole_grid**2 + z_hole_grid**2 <= radius**2)

        # Вырежьте отверстия в кубе
        x[mask] = np.nan
        y[mask] = np.nan
        z[mask] = np.nan

        holes.append((x_hole, y_hole, z_hole, radius, depth))

    return x, y, z, holes

# Визуализируйте поверхность
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y, z = generate_cube(-5, 5, -5, 5, -5, 5, 100, 100, 100)
x, y, z, holes = create_holes(x, y, z, 2, 2)

# Удалите значения NaN (отверстия) из визуализации
x = np.nan_to_num(x)
y = np.nan_to_num(y)
z = np.nan_to_num(z)

# Визуализируйте куб с отверстиями
ax.scatter(x, y, z, c='b', alpha=0.5)

# Визуализируйте отверстия
for hole in holes:
    x_hole, y_hole, z_hole, radius, depth = hole
    ax.scatter(x_hole, y_hole, z_hole, c='r', s=radius*100, alpha=0.5)

#Сохраните файл в формате OBJ
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "cube_with_holes.obj")
with open(filename, "w") as f:
    f.write("# cube_with_holes.obj\n")
    for i in range(len(x)):
        for j in range(len(y)):
            for k in range(len(z)):
                if not np.isnan(x[i, j, k]):
                    f.write(f"v {x[i, j, k]} {y[i, j, k]} {z[i, j, k]}\n")
    for i in range(len(x) - 1):
        for j in range(len(y) - 1):
            for k in range(len(z) - 1):
                if not np.isnan(x[i, j, k]) and not np.isnan(x[i + 1, j, k]) and not np.isnan(x[i, j + 1, k]) and not np.isnan(x[i, j, k + 1]):
                    f.write(f"f {i * len(y) * len(z) + j * len(z) + k + 1} {(i + 1) * len(y) * len(z) + j * len(z) + k + 1} {(i + 1) * len(y) * len(z) + (j + 1) * len(z) + k + 1}\n")
                    f.write(f"f {i * len(y) * len(z) + j * len(z) + k + 1} {(i + 1) * len(y) * len(z) + (j + 1) * len(z) + k + 1} {i * len(y) * len(z) + (j + 1) * len(z) + k + 1}\n")

plt.show()
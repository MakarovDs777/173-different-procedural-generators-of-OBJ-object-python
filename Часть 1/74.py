import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy import ndimage
import trimesh
import os
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

        # Создаем дырку с правильным радиусом и глубиной
        x_hole_grid = np.linspace(x_hole - radius, x_hole + radius, 100)
        y_hole_grid = np.linspace(y_hole - radius, y_hole + radius, 100)
        x_hole_grid, y_hole_grid = np.meshgrid(x_hole_grid, y_hole_grid)
        z_hole_grid = np.zeros((100, 100))
        x_hole_grid, y_hole_grid, z_hole_grid = ndimage.gaussian_filter(x_hole_grid, sigma=1), ndimage.gaussian_filter(y_hole_grid, sigma=1), ndimage.gaussian_filter(z_hole_grid, sigma=1)
        x_hole_grid, y_hole_grid, z_hole_grid = ndimage.gaussian_filter(x_hole_grid, sigma=1), ndimage.gaussian_filter(y_hole_grid, sigma=1), ndimage.gaussian_filter(z_hole_grid, sigma=1)
        x_hole_grid, y_hole_grid, z_hole_grid = ndimage.gaussian_filter(x_hole_grid, sigma=1), ndimage.gaussian_filter(y_hole_grid, sigma=1), ndimage.gaussian_filter(z_hole_grid, sigma=1)

        # Смещаем дырку на поверхность
        x_min = x_hole_grid.min()
        x_max = x_hole_grid.max()
        y_min = y_hole_grid.min()
        y_max = y_hole_grid.max()
        for i in range(int(x.shape[0])):
            for j in range(int(x.shape[1])):
                if x[i, j] >= x_min and x[i, j] <= x_max and y[i, j] >= y_min and y[i, j] <= y_max:
                    z[i, j] = -depth

        holes.append((x_hole, y_hole, radius, depth))

    return x, y, z, holes

# Визуализация поверхности
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y, z = generate_surface(-10, 10, -10, 10, 100, 100)
x, y, z, holes = create_holes(x, y, z, 5, 5)

ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5)
for hole in holes:
    x_hole, y_hole, radius, depth = hole
    x_min = x_hole - radius
    x_max = x_hole + radius
    y_min = y_hole - radius
    y_max = y_hole + radius
    ax.bar3d(x_min, y_min, -depth, x_max-x_min, y_max-y_min, 0, color='r', alpha=0.5)

# Создание 3D-модели
mesh = trimesh.Trimesh(vertices=np.column_stack((x.flatten(), y.flatten(), z.flatten())), faces=np.array([(i, i+1, i+len(x)) for i in range(len(x)*len(y)-len(x))]))

# Экспорт 3D-модели в формат OBJ
mesh.export(os.path.join(os.path.expanduser("~"), "Desktop", 'urface_with_holes.obj'))

plt.show()

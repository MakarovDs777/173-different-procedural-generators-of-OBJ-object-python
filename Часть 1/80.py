import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_maze(shape, wall_density):
    # Создаем 3D массив для лабиринта
    maze = np.ones(shape, dtype=float)

    # Генерируем стены в лабиринте
    for x in range(shape[0]):
        for y in range(shape[1]):
            if np.random.rand() < wall_density:
                maze[x, y, :] = 0.0

    return maze

def generate_floor_surface(shape, floor_z):
    # Создаем 3D массив для пола
    floor = np.zeros(shape, dtype=float)

    # Генерируем пол на заданной высоте
    for x in range(shape[0]):
        for y in range(shape[1]):
            floor[x, y, floor_z] = 1.0

    return floor

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
wall_density = 0.2  # Плотность стен
floor_z = 0  # Высота пола

# Генерация лабиринта
maze = generate_maze(shape, wall_density)

# Генерация пола под лабиринтом
floor = generate_floor_surface(shape, floor_z)

# Объединение лабиринта и пола логическим оператором "или"
maze = np.logical_or(maze, floor).astype(float)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(maze, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "maze.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)
plt.show()
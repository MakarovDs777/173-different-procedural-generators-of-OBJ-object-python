import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_labyrinth(shape, wall_density, wall_height):
    # Создаем 3D массив для лабиринта
    labyrinth = np.zeros(shape, dtype=bool)

    # Генерируем стены лабиринта
    for x in range(shape[0]):
        for y in range(shape[1]):
            if np.random.rand() < wall_density:
                for z in range(wall_height):
                    labyrinth[x, y, z] = True

    # Создаем сквозные проходы через потолок и пол
    for x in range(shape[0]):
        for y in range(shape[1]):
            if labyrinth[x, y, 0]:
                for z in range(1, wall_height):
                    labyrinth[x, y, z] = False
            if labyrinth[x, y, shape[2] - 1]:
                for z in range(shape[2] - 2, 0, -1):
                    labyrinth[x, y, z] = False

    return labyrinth

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
wall_density = 0.1  # Плотность стен
wall_height = 10  # Высота стен

# Генерация лабиринта
labyrinth = generate_labyrinth(shape, wall_density, wall_height)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(labyrinth.astype(float), level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "labyrinth.obj")
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

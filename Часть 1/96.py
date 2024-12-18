import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

# Функция для генерации лабиринта
def generate_maze(shape, direction):
    maze = np.ones(shape, dtype=float)

    def recursive_divide(x, y, z, w, h, d):
        if w < 2 or h < 2 or d < 2:
            return
        if direction == "left_to_right":
            if w > 2:
                wall_x = np.random.randint(x + 1, x + w - 1)
                for i in range(y, y + h):
                    for j in range(z, z + d):
                        maze[wall_x, i, j] = 0.0
                recursive_divide(x, y, z, wall_x - x, h, d)
                recursive_divide(wall_x + 1, y, z, x + w - wall_x - 1, h, d)
        elif direction == "back_to_front":
            if h > 2:
                wall_y = np.random.randint(y + 1, y + h - 1)
                for i in range(x, x + w):
                    for j in range(z, z + d):
                        maze[i, wall_y, j] = 0.0
                recursive_divide(x, y, z, w, wall_y - y, d)
                recursive_divide(x, wall_y + 1, z, w, y + h - wall_y - 1, d)
        elif direction == "top_to_bottom":
            if d > 2:
                wall_z = np.random.randint(z + 1, z + d - 1)
                for i in range(x, x + w):
                    for j in range(y, y + h):
                        maze[i, j, wall_z] = 0.0
                recursive_divide(x, y, z, w, h, wall_z - z)
                recursive_divide(x, y, wall_z + 1, w, h, z + d - wall_z - 1)

    recursive_divide(0, 0, 0, shape[0], shape[1], shape[2])

    return maze

# Параметры
shape = (64, 64, 64)

# Генерация лабиринтов
maze_left_to_right = generate_maze(shape, "left_to_right")
maze_back_to_front = generate_maze(shape, "back_to_front")
maze_top_to_bottom = generate_maze(shape, "top_to_bottom")

# Объединение лабиринтов логическим оператором "и" (AND)
combined_maze = np.logical_and(np.logical_and(maze_left_to_right, maze_back_to_front), maze_top_to_bottom).astype(float)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(combined_maze, level=0.5)

# Объединение вершин и граней в один объект
verts = np.concatenate((verts, verts + [shape[0], 0, 0], verts + [0, shape[1], 0], verts + [0, 0, shape[2]]))
faces = np.concatenate((faces, faces + [len(verts) // 3, len(verts) // 3 + 1, len(verts) // 3 + 2]))

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "combined_maze.obj")
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
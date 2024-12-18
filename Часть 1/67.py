import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def generate_cube_field(shape):
    array = np.zeros(shape, dtype=float)
    # Создаем куб, заполняя массив значениями
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                # Преобразуем координаты в диапазон (-1, 1)
                xf = (x / shape[0]) * 2 - 1
                yf = (y / shape[1]) * 2 - 1
                zf = (z / shape[2]) * 2 - 1
                # Вычисляем значение куба
                if abs(xf) < 0.5 and abs(yf) < 0.5 and abs(zf) < 0.5:
                    value = 1.0
                else:
                    value = 0.0
                array[x, y, z] = value
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива

# Генерация 3D-поля
cube_field = generate_cube_field(shape)

# Создание куба
verts = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
])

faces = np.array([
    [0, 1, 2],
    [0, 2, 3],
    [4, 5, 6],
    [4, 6, 7],
    [0, 1, 5],
    [0, 5, 4],
    [1, 2, 6],
    [1, 6, 5],
    [2, 3, 7],
    [2, 7, 6],
    [3, 0, 4],
    [3, 4, 7]
])

# Сохранение куба в OBJ файл
mesh = trimesh.Trimesh(vertices=verts, faces=faces)
mesh.export("cube.obj")
# Параметры
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "cube.obj")

# Ви
# Сохранение изосурфейса в OBJ файл
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(verts[:, 0], verts[:, 1], verts[:, 2], color='r', alpha=0.5)
for face in faces:
    v1, v2, v3 = verts[face]
    ax.plot3D([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], 'r', alpha=0.5)
    ax.plot3D([v2[0], v3[0]], [v2[1], v3[1]], [v2[2], v3[2]], 'r', alpha=0.5)
    ax.plot3D([v3[0], v1[0]], [v3[1], v1[1]], [v3[2], v1[2]], 'r', alpha=0.5)
plt.show()
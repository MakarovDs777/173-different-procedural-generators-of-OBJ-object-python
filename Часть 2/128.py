import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os

def generate_room():
    # Определите размеры комнаты
    width = 100
    height = 2
    depth = 100

    # Определите вершины комнаты
    vertices = [
        [0, 0, 0],
        [width, 0, 0],
        [width, 0, depth],
        [0, 0, depth],
        [0, height, 0],
        [width, height, 0],
        [width, height, depth],
        [0, height, depth]
    ]

    # Определите грани комнаты
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7]
    ]

    mesh = trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
    return mesh

def generate_cubes_field(shape, num_cubes):
    array = np.ones(shape, dtype=float)
    # Генерируем кубы внутри куба
    for _ in range(num_cubes):
        # Выбираем случайную позицию на верхней стороне
        x = np.random.randint(0, shape[0])
        y = np.random.randint(0, shape[1])
        z = np.random.randint(0, shape[2])
        # Генерируем куб, который проходит от верхней стороны к нижней стороне
        for i in range(max(0, x-1), min(shape[0], x+2)):
            for j in range(max(0, y-1), min(shape[1], y+2)):
                for k in range(max(0, z-1), min(shape[2], z+2)):
                    if abs(i - x) <= 1 and abs(j - y) <= 1 and abs(k - z) <= 1:
                        array[i, j, k] = 0.0
    return array

# Генерация комнаты
room = generate_room()

# Генерация массива с дырками
array = generate_cubes_field((100, 100, 2), 100)

# Создание меша с дырками
vertices = []
faces = []
for i in range(array.shape[0]):
    for j in range(array.shape[1]):
        for k in range(array.shape[2]):
            if array[i, j, k] == 1:
                vertices.extend([
                    [i, j, k],
                    [i+1, j, k],
                    [i+1, j+1, k],
                    [i, j+1, k],
                    [i, j, k+1],
                    [i+1, j, k+1],
                    [i+1, j+1, k+1],
                    [i, j+1, k+1]
                ])
                faces.extend([
                    [len(vertices)-8, len(vertices)-7, len(vertices)-6, len(vertices)-5],
                    [len(vertices)-4, len(vertices)-3, len(vertices)-2, len(vertices)-1],
                    [len(vertices)-8, len(vertices)-7, len(vertices)-3, len(vertices)-4],
                    [len(vertices)-7, len(vertices)-6, len(vertices)-2, len(vertices)-3],
                    [len(vertices)-6, len(vertices)-5, len(vertices)-1, len(vertices)-2],
                    [len(vertices)-5, len(vertices)-4, len(vertices)-8, len(vertices)-1]
                ])

mesh = trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "room_with_holes.obj")
mesh.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.add_collection3d(mesh)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_zlim(0, 2)
plt.show()

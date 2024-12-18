import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_hair(shape, hair_density, direction):
    # Создаем 3D массив для волос
    hair = np.zeros(shape, dtype=float)

    # Генерируем волосы в заданном направлении
    for x in range(shape[0]):
        for y in range(shape[1]):
            if np.random.rand() < hair_density:
                if direction == 'up':
                    hair[x, y, :] = np.linspace(0, 1, shape[2])
                elif direction == 'down':
                    hair[x, y, :] = np.linspace(1, 0, shape[2])
                elif direction == 'left':
                    hair[:, x, y] = np.linspace(0, 1, shape[0])
                elif direction == 'right':
                    hair[:, x, y] = np.linspace(1, 0, shape[0])

    return hair

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
hair_density = 0.1  # Плотность волос
floor_z = 0  # Высота пола

# Генерация волос вверх
hair_up = generate_hair(shape, hair_density, 'up')

# Генерация волос вниз
hair_down = generate_hair(shape, hair_density, 'down')

# Генерация волос влево
hair_left = generate_hair(shape, hair_density, 'left')

# Генерация волос вправо
hair_right = generate_hair(shape, hair_density, 'right')

# Генерация пола под волосами
floor = generate_floor_surface(shape, floor_z)

# Объединение волос и пола логическим оператором "или"
hair = np.logical_or(np.logical_or(np.logical_or(hair_up, hair_down), np.logical_or(hair_left, hair_right)), floor).astype(float)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(hair, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "hair.obj")
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

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_hair_field(shape, num_hairs, hair_length, hair_radius):
    array = np.zeros(shape, dtype=float)
    for _ in range(num_hairs):
        x, y, z = np.random.randint(0, shape[0]), np.random.randint(0, shape[1]), np.random.randint(0, shape[2])
        for _ in range(hair_length):
            dx = np.random.randint(-1, 2)
            dy = np.random.randint(-1, 2)
            dz = np.random.randint(1, 3)
            x += dx
            y += dy
            z += dz
            if 0 <= x < shape[0] and 0 <= y < shape[1] and 0 <= z < shape[2]:
                array[x, y, z] = 1.0
                # Делаем волосы более жирными
                if x > 0:
                    array[x-1, y, z] = 1.0
                if x < shape[0] - 1:
                    array[x+1, y, z] = 1.0
                if y > 0:
                    array[x, y-1, z] = 1.0
                if y < shape[1] - 1:
                    array[x, y+1, z] = 1.0
                if z > 0:
                    array[x, y, z-1] = 1.0
                if z < shape[2] - 1:
                    array[x, y, z+1] = 1.0
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
num_hairs = 100  # Количество волос
hair_length = 20  # Длина волос
hair_radius = 1  # Радиус волос

# Генерация 3D-поля с волосами
hair_field = generate_hair_field(shape, num_hairs, hair_length, hair_radius)

# Создание изосурфейса из 3D-поля
verts, faces, _, _ = measure.marching_cubes(hair_field, level=0.5)

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
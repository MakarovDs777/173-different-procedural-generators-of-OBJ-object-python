import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_spheres_field(shape, num_spheres, min_radius, max_radius):
    array = np.ones(shape, dtype=float)
    # Генерируем сферы внутри куба
    for _ in range(num_spheres):
        x = np.random.randint(0, shape[0])
        y = np.random.randint(0, shape[1])
        z = np.random.randint(0, shape[2])
        radius = np.random.uniform(min_radius, max_radius)
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    distance = np.sqrt((i - x) ** 2 + (j - y) ** 2 + (k - z) ** 2)
                    if distance < radius:
                        array[i, j, k] = 0.0
    return array

def generate_cube_field(shape):
    array = np.ones(shape, dtype=float)
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
num_spheres = 500  # Количество сфер
min_radius = 2  # Минимальный радиус сферы
max_radius = 10  # Максимальный радиус сферы

# Генерация 3D-поля с сферами
spheres_field = generate_spheres_field(shape, num_spheres, min_radius, max_radius)

# Генерация 3D-поля с кубом
cube_field = generate_cube_field(shape)

# Объединение полей
field = np.minimum(spheres_field, cube_field)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "cheese.obj")
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
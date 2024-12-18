import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_hair_surface(shape, hair_length, hair_density):
    # Создаем 3D массив для поверхности
    surface = np.zeros(shape, dtype=float)

    # Генерируем волосы на поверхности
    for x in range(shape[0]):
        for y in range(shape[1]):
            if np.random.rand() < hair_density:
                hair_x = x
                hair_y = y
                hair_z = 0
                for z in range(hair_length):
                    surface[hair_x, hair_y, z] = 1.0
                    # Делаем волосы более жирными
                    if hair_x > 0:
                        surface[hair_x-1, hair_y, z] = 1.0
                    if hair_x < shape[0] - 1:
                        surface[hair_x+1, hair_y, z] = 1.0
                    if hair_y > 0:
                        surface[hair_x, hair_y-1, z] = 1.0
                    if hair_y < shape[1] - 1:
                        surface[hair_x, hair_y+1, z] = 1.0

    return surface

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
hair_length = 10  # Длина волос
hair_density = 0.1  # Плотность волос

# Генерация поверхности с волосами
hair_surface = generate_hair_surface(shape, hair_length, hair_density)

# Объединение поверхностей логическим оператором "или"
surface = hair_surface.astype(float)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(surface, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "lines.obj")
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
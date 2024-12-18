import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_lines_field(shape):
    array = np.zeros(shape, dtype=float)
    # Генерируем ломанную линию внутри куба
    x, y, z = np.random.randint(0, shape[0]), np.random.randint(0, shape[1]), np.random.randint(0, shape[2])
    for _ in range(100):  # количество сегментов ломанной линии
        dx = np.random.randint(-5, 6)
        dy = np.random.randint(-5, 6)
        dz = np.random.randint(-5, 6)
        length = int(np.sqrt(dx**2 + dy**2 + dz**2))
        for i in range(length):
            new_x = x + i * dx // length
            new_y = y + i * dy // length
            new_z = z + i * dz // length
            if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                array[new_x, new_y, new_z] = 1.0
                # Делаем линии более жирными
                if new_x > 0:
                    array[new_x-1, new_y, new_z] = 1.0
                if new_x < shape[0] - 1:
                    array[new_x+1, new_y, new_z] = 1.0
                if new_y > 0:
                    array[new_x, new_y-1, new_z] = 1.0
                if new_y < shape[1] - 1:
                    array[new_x, new_y+1, new_z] = 1.0
                if new_z > 0:
                    array[new_x, new_y, new_z-1] = 1.0
                if new_z < shape[2] - 1:
                    array[new_x, new_y, new_z+1] = 1.0
        x, y, z = new_x, new_y, new_z
    return array

def generate_cube_field(shape):
    array = np.ones(shape, dtype=float)
    # Удаляем все 6 сторон куба
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                if x == 0 or x == shape[0] - 1 or y == 0 or y == shape[1] - 1 or z == 0 or z == shape[2] - 1:
                    array[x, y, z] = 0.0
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива

# Генерация 3D-поля с линиями
lines_field = generate_lines_field(shape)

# Генерация 3D-поля с кубом
cube_field = generate_cube_field(shape)

# Объединение полей логическим оператором "или"
field = np.logical_and(lines_field, cube_field).astype(float)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(field, level=0.5)

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

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_lines_field(shape, num_lines):
    array = np.ones(shape, dtype=float)
    # Генерируем линии внутри куба
    for _ in range(num_lines):
        x1 = np.random.randint(0, shape[0])
        y1 = np.random.randint(0, shape[1])
        z1 = np.random.randint(0, shape[2])
        x2 = np.random.randint(0, shape[0])
        y2 = np.random.randint(0, shape[1])
        z2 = np.random.randint(0, shape[2])
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        length = int(np.sqrt(dx**2 + dy**2 + dz**2))
        for i in range(length):
            x = x1 + i * dx // length
            y = y1 + i * dy // length
            z = z1 + i * dz // length
            if 0 <= x < shape[0] and 0 <= y < shape[1] and 0 <= z < shape[2]:
                array[x, y, z] = 0.0
                # Делаем линии более жирными
                if x > 0:
                    array[x-1, y, z] = 0.0
                if x < shape[0] - 1:
                    array[x+1, y, z] = 0.0
                if y > 0:
                    array[x, y-1, z] = 0.0
                if y < shape[1] - 1:
                    array[x, y+1, z] = 0.0
                if z > 0:
                    array[x, y, z-1] = 0.0
                if z < shape[2] - 1:
                    array[x, y, z+1] = 0.0
    return array

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
num_lines = 100  # Количество линий

# Генерация 3D-поля с линиями
lines_field = generate_lines_field(shape, num_lines)

# Генерация 3D-поля с кубом
cube_field = generate_cube_field(shape)

# Объединение полей
field = np.minimum(lines_field, cube_field)

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

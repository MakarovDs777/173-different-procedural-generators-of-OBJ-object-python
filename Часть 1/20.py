import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_cubes_field(shape, num_cubes, min_size, max_size):
    array = np.ones(shape, dtype=float)
    # Генерируем кубы внутри куба
    for _ in range(num_cubes):
        x = np.random.randint(0, shape[0])
        y = np.random.randint(0, shape[1])
        z = np.random.randint(0, shape[2])
        size = np.random.randint(min_size, max_size + 1)
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    if abs(i - x) < size // 2 and abs(j - y) < size // 2 and abs(k - z) < size // 2:
                        # Создаем пустые крести внутри куба
                        xf = (i - x) / (size // 2)
                        yf = (j - y) / (size // 2)
                        zf = (k - z) / (size // 2)
                        if abs(xf) < 0.1 or abs(yf) < 0.1 or abs(zf) < 0.1:
                            array[i, j, k] = 0.0
                        else:
                            array[i, j, k] = 1.0
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
                    array[x, y, z] = 1.0
                else:
                    array[x, y, z] = 0.0
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
num_cubes = 500  # Количество кубов
min_size = 2  # Минимальный размер куба
max_size = 10  # Максимальный размер куба

# Генерация 3D-поля с кубами
cubes_field = generate_cubes_field(shape, num_cubes, min_size, max_size)

# Генерация 3D-поля с кубом
cube_field = generate_cube_field(shape)

# Объединение полей
field = np.minimum(cubes_field, cube_field)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "sponge.obj")
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
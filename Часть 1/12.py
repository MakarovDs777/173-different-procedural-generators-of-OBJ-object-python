import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_fractal_field(shape, scale):
    array = np.zeros(shape, dtype=float)
    # Создаем фрактал, заполняя массив значениями
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                # Преобразуем координаты в диапазон (-1, 1)
                xf = (x / shape[0]) * 2 - 1
                yf = (y / shape[1]) * 2 - 1
                zf = (z / shape[2]) * 2 - 1
                # Вычисляем значение фрактала
                value = np.sin(10 * np.sqrt(xf**2 + yf**2 + zf**2)) * np.cos(10 * xf) * np.sin(10 * yf) * np.cos(10 * zf)
                array[x, y, z] = value
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
scale = 2  # Масштабирование координат для массива

# Генерация 3D-поля
fractal_field = generate_fractal_field(shape, scale)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(fractal_field, level=0.0)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "fractal.obj")
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
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_tube_field(shape, num_tubes, tube_length, tube_radius):
    array = np.zeros(shape, dtype=float)
    for _ in range(num_tubes):
        # Параметры кривой
        x0, y0, z0 = np.random.randint(0, shape[0]), np.random.randint(0, shape[1]), np.random.randint(0, shape[2])
        r = np.random.randint(10, 20)  # радиус окружности
        theta = np.linspace(0, 2 * np.pi, tube_length)

        # Создаем кривую
        x = x0 + r * np.cos(theta)
        y = y0 + r * np.sin(theta)
        z = np.linspace(z0, z0 + tube_length, tube_length)

        # Заполняем массив
        for i in range(tube_length):
            if 0 <= x[i] < shape[0] and 0 <= y[i] < shape[1] and 0 <= z[i] < shape[2]:
                # Создайте двумерную гауссову функцию для круглого поперечного сечения
                xx, yy = np.meshgrid(np.arange(shape[0]) - x[i], np.arange(shape[1]) - y[i])
                gaussian = (1 / (2 * np.pi * tube_radius ** 2)) * np.exp(-(xx ** 2 + yy ** 2) / (2 * tube_radius ** 2))
                array[int(z[i]), :, :] += gaussian
    return array

# Параметры
shape = (64, 64, 64)  # Размеры трехмерного массива
num_tubes = 5  # Количество трубок
tube_length = 64  # Длина труб
tube_radius = 3  # Радиус труб

# Создание трехмерного поля круглых трубок
tube_field = generate_tube_field(shape, num_tubes, tube_length, tube_radius)

# Создание изоповерхности из трехмерного поля
verts, faces, _, _ = measure.marching_cubes(tube_field, level=0.5 * np.max(tube_field))

# Сохраните изурфейс в OBJ-файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "round_tube.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]:.4f} {vert[1]:.4f} {vert[2]:.4f}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

# Визуализация 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)
plt.show()
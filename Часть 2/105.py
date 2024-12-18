import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

# Функция для генерации 3D-поля с коридорами
def generate_delaunay_field(shape):
    array = np.zeros(shape, dtype=float)

    # Генерация точек для коридоров
    points = []
    for _ in range(10):
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        points.append([x, y, shape[2] // 2])  # Генерация точек на фиксированной высоте

    # Генерация коридоров между точками
    radius = 10  # Радиус вздутия
    for i in range(len(points) - 1):
        x1, y1, z1 = points[i]
        x2, y2, z2 = points[i + 1]
        
        # Линейная интерполяция между точками
        for t in np.linspace(0, 1, num=10):
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)
            z = z1  # Поддерживаем фиксированную высоту
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    for dz in range(-radius, radius + 1):
                        if dx**2 + dy**2 + dz**2 <= radius**2:  # Проверка на попадание в сферу
                            if 0 <= x + dx < shape[0] and 0 <= y + dy < shape[1] and 0 <= z + dz < shape[2]:
                                array[x + dx, y + dy, z + dz] = 1.0

    return array

# Параметры
shape = (128, 128, 128)  # Размеры 3D массива

# Генерация 3D-поля с коридорами
delaunay_field = generate_delaunay_field(shape)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(delaunay_field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "delaunay.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]:.4f} {vert[1]:.4f} {vert[2]:.4f}\n")
    for face in faces:
        f.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], color='r', alpha=0.5)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

# Функция для генерации 3D-поля с трубками
def generate_tube_field(shape, tube_radius):
    array = np.zeros(shape, dtype=float)

    # Генерация точек для трубок
    points = []
    for _ in range(10):
        x = np.random.randint(tube_radius, shape[0] - tube_radius)
        y = np.random.randint(tube_radius, shape[1] - tube_radius)
        points.append([x, y, shape[2] // 2])  # Генерируем точки на фиксированной высоте

    # Генерация трубок между точками
    for i in range(len(points) - 1):
        dx = points[i + 1][0] - points[i][0]
        dy = points[i + 1][1] - points[i][1]
        length = int(np.sqrt(dx**2 + dy**2))
        
        for j in range(length + 1):  # Проход по всей длине трубки
            # Прямое смещение до следующей точки
            new_x = int(points[i][0] + j * dx // length)
            new_y = int(points[i][1] + j * dy // length)
            new_z = int(points[i][2])

            # Создание поперечного сечения трубки
            for k in range(-tube_radius, tube_radius + 1):
                for l in range(-tube_radius, tube_radius + 1):
                    if k**2 + l**2 <= tube_radius**2:  # Убедиться, что мы находимся в пределах радиуса трубки
                        x1, y1, z1 = new_x + k, new_y + l, new_z
                        if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                            array[x1, y1, z1] = 1.0

    return array

# Параметры
shape = (128, 128, 128)  # Размеры 3D массива
tube_radius = 3          # Радиус трубки

# Генерация 3D-поля с трубками
delaunay_field = generate_tube_field(shape, tube_radius)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(delaunay_field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "tubes.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]:.4f} {vert[1]:.4f} {vert[2]:.4f}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], color='r', alpha=0.5)
plt.show()


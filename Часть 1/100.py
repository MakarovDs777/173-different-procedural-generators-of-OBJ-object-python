import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from scipy.spatial import Delaunay
import os

# Функция для генерации 3D-поля с коридорами
def generate_delaunay_field(shape):
    array = np.zeros(shape, dtype=float)

    # Генерация точек для коридоров
    points = []
    for _ in range(10):
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        points.append([x, y, shape[2] // 2])  # Генерируем точки на фиксированной высоте

    # Генерация коридоров между точками
    for i in range(len(points) - 1):
        dx = points[i+1][0] - points[i][0]
        dy = points[i+1][1] - points[i][1]
        length = max(abs(dx), abs(dy))
        if abs(dx) > abs(dy):
            for j in range(length):
                new_x = int(points[i][0] + j * dx // length)
                new_y = points[i][1]
                new_z = int(points[i][2])
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        x1, y1, z1 = new_x + k, new_y + l, new_z
                        if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                            array[x1, y1, z1] = 1.0
        else:
            for j in range(length):
                new_x = points[i][0]
                new_y = int(points[i][1] + j * dy // length)
                new_z = int(points[i][2])
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        x1, y1, z1 = new_x + k, new_y + l, new_z
                        if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                            array[x1, y1, z1] = 1.0

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
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], color='r', alpha=0.5)
plt.show()

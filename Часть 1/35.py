import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import Delaunay
import os

# Функция для генерации 3D-линии с триангуляцией Делоне
def generate_delaunay_line(shape):
    points = []
    for i in range(100):
        x = np.random.uniform(0, shape[0])
        y = np.random.uniform(0, shape[1])
        z = np.random.uniform(0, shape[2])
        points.append([x, y, z])

    # Преобразование точек в NumPy массив 
    points = np.array(points)

    # Выполнить триангуляцию Делоне
    triangulation = Delaunay(points)

    # Постройте график треугольников
    for triangle in triangulation.simplices:
        for i in range(3):
            dx = points[triangle[(i+1)%3], 0] - points[triangle[i], 0]
            dy = points[triangle[(i+1)%3], 1] - points[triangle[i], 1]
            dz = points[triangle[(i+1)%3], 2] - points[triangle[i], 2]
            length = int(np.sqrt(dx**2 + dy**2 + dz**2))
            for j in range(length):
                new_x = int(points[triangle[i], 0] + j * dx // length)
                new_y = int(points[triangle[i], 1] + j * dy // length)
                new_z = int(points[triangle[i], 2] + j * dz // length)
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    # Добавить точку в список точек
                    points = np.append(points, [[new_x, new_y, new_z]], axis=0)

    return points

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива

# Генерация 3D-линии с триангуляцией Делоне
points = generate_delaunay_line(shape)

# Создание изосурфейса
verts = np.array(points)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "delaunay_line.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for i in range(len(verts) - 1):
        f.write(f"l {i+1} {i+2}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(*zip(*verts), 'b-')
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import Delaunay
import os

# Функция для генерации 3D-трубки с триангуляцией Делоне
def generate_delaunay_tube(shape):
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

    # Создание трубки
    tube_points = []
    tube_faces = []
    for triangle in triangulation.simplices:
        for i in range(3):
            x1, y1, z1 = points[triangle[i]]
            x2, y2, z2 = points[triangle[(i+1)%3]]
            vec = np.array([x2-x1, y2-y1, z2-z1])
            vec = vec / np.linalg.norm(vec)
            perp_vec1 = np.array([vec[1], -vec[0], 0])
            perp_vec1 = perp_vec1 / np.linalg.norm(perp_vec1)
            perp_vec2 = np.cross(vec, perp_vec1)
            perp_vec2 = perp_vec2 / np.linalg.norm(perp_vec2)
            radius = 5
            num_points = 10
            angles = np.linspace(0, 2*np.pi, num_points)
            for k in range(num_points):
                pos1 = np.array([x1, y1, z1]) + radius * (np.cos(angles[k]) * perp_vec1 + np.sin(angles[k]) * perp_vec2)
                pos2 = np.array([x2, y2, z2]) + radius * (np.cos(angles[k]) * perp_vec1 + np.sin(angles[k]) * perp_vec2)
                tube_points.append(pos1.tolist())
                tube_points.append(pos2.tolist())
                tube_faces.append([len(tube_points)-2, len(tube_points)-1, len(tube_points)])
                tube_faces.append([len(tube_points)-1, len(tube_points)-2, len(tube_points)])

    return tube_points, tube_faces

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива

# Генерация 3D-трубки с триангуляцией Делоне
tube_points, tube_faces = generate_delaunay_tube(shape)

# Сохранение трубки в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "delaunay_tube.obj")
with open(filename, "w") as f:
    for j, point in enumerate(tube_points):
        f.write(f"v {point[0]} {point[1]} {point[2]}\n")
    for face in tube_faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for j in range(len(tube_points) - 1):
    ax.plot3D(*zip(tube_points[j], tube_points[j+1]), 'b-')
plt.show()
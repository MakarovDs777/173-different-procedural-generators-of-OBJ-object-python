import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import random
import os

# Функция для генерации кадра
def update(ax, i):
    ax.clear()  # Очистка текущего окна

    # Генерация линии
    points = []
    for j in range(100):
        x = np.random.uniform(-100, 100)
        y = np.random.uniform(-100, 100)
        z = np.random.uniform(-100, 100)
        points.append([x, y, z])

    # Создание трубки
    tube_vertices = []
    tube_faces = []
    for j in range(len(points) - 1):
        x1, y1, z1 = points[j]
        x2, y2, z2 = points[j+1]
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
            tube_vertices.append(pos1.tolist())
            tube_vertices.append(pos2.tolist())

            # Создание граней для трубки
            if k == 0:
                tube_faces.append([j*2, j*2+1, (j+1)*2])
            elif k == num_points - 1:
                tube_faces.append([j*2+1, (j+1)*2, (j+1)*2+1])
            else:
                tube_faces.append([j*2+1, (j+1)*2, (j+1)*2+1, j*2+1])

    # Отрисовка трубки
    ax.plot_trisurf(*zip(*tube_vertices), triangles=tube_faces, color='b')

    # Сохранение трубки в файл OBJ
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, f"tube_{i+1}.obj")
    with open(filename, "w") as f:
        for j, vertex in enumerate(tube_vertices):
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in tube_faces:
            f.write(f"f {{{' '.join(str(v+1) for v in face)}}}\n")
    print(f"Model saved as {filename}")

# Запуск анимации
plt.ion()  # Включение интерактивного режима
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-150, 150)
ax.set_ylim(-150, 150)
ax.set_zlim(-150, 150)

for i in range(100):
    update(ax, i)
    plt.pause(5)  # Пауза между кадрами
    plt.draw()  # Отрисовка текущего кадра

plt.ioff()  # Выключение интерактивного режима
plt.show()  # Окончательный кадр
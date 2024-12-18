import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import random
import os

# Функция для генерации кадра
def update(ax, i):
    ax.clear()  # Очистка текущего окна

    # Генерация изогнутой линии
    t = np.linspace(0, 2*np.pi, 100)
    x = np.cos(t)
    y = np.sin(t)
    z = np.sin(2*t)

    points = np.array([x, y, z]).T

    # Создание трубки
    tube_points = []
    for i, point in enumerate(points):
        if i < len(points) - 1:
            x1, y1, z1 = point
            x2, y2, z2 = points[i+1]
            vec = np.array([x2-x1, y2-y1, z2-z1])
            vec = vec / np.linalg.norm(vec)
            perp_vec1 = np.array([vec[1], -vec[0], 0])
            perp_vec1 = perp_vec1 / np.linalg.norm(perp_vec1)
            perp_vec2 = np.cross(vec, perp_vec1)
            perp_vec2 = perp_vec2 / np.linalg.norm(perp_vec2)
            radius = 0.5
            num_points = 20
            angles = np.linspace(0, 2*np.pi, num_points)
            for k in range(num_points):
                pos = np.array([x1, y1, z1]) + radius * (np.cos(angles[k]) * perp_vec1 + np.sin(angles[k]) * perp_vec2)
                tube_points.append(pos.tolist())
        else:
            x1, y1, z1 = point
            radius = 0.5
            num_points = 20
            angles = np.linspace(0, 2*np.pi, num_points)
            for k in range(num_points):
                pos = np.array([x1, y1, z1]) + radius * (np.cos(angles[k]) * np.array([1, 0, 0]) + np.sin(angles[k]) * np.array([0, 1, 0]))
                tube_points.append(pos.tolist())

    # Отрисовка трубки
    for i in range(0, len(tube_points), 20):
        for j in range(20):
            if j < 19:
                ax.plot3D(*zip(tube_points[i+j], tube_points[i+j+1]), 'b-')
            else:
                ax.plot3D(*zip(tube_points[i+j], tube_points[i]), 'b-')
        if i < len(tube_points) - 20:
            for j in range(20):
                ax.plot3D(*zip(tube_points[i+j], tube_points[i+20+j]), 'b-')

    # Сохранение трубки в файл OBJ
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, f"tube_{i+1}.obj")
    with open(filename, "w") as f:
        for j, point in enumerate(tube_points):
            f.write(f"v {point[0]} {point[1]} {point[2]}\n")
        for i in range(0, len(tube_points), 20):
            for j in range(20):
                if j < 19:
                    f.write(f"f {i+j+1} {i+j+2} {i+20+j+1}\n")
                    f.write(f"f {i+j+2} {i+j+1} {i+20+j+2}\n")
            if i < len(tube_points) - 20:
                for j in range(20):
                    f.write(f"f {i+j+1} {i+j+2} {i+20+j+1}\n")
                    f.write(f"f {i+j+2} {i+j+1} {i+20+j+2}\n")
    print(f"Model saved as {filename}")

    # Отрисовка трубки
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    plt.draw()

# Запуск анимации
plt.ion()  # Включение интерактивного режима
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

for i in range(100):
    update(ax, i)
    plt.pause(5)  # Пауза между кадрами
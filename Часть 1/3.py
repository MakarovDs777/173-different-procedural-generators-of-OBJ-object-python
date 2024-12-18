import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import random
import os

# Функция для генерации кадра
def update(ax):
    ax.clear()  # Очистка текущего окна

    # Генерация линии
    points = []
    for i in range(100):
        x = np.random.uniform(-100, 100)
        y = np.random.uniform(-100, 100)
        z = np.random.uniform(-100, 100)
        points.append([x, y, z])

    for i in range(len(points) - 1):
        ax.plot([points[i][0], points[i+1][0]], [points[i][1], points[i+1][1]], [points[i][2], points[i+1][2]], 'b-', linewidth=5)

    return points

# Функция для сохранения ломаной линии в файл OBJ
def save_to_obj(points, filename):
    with open(filename, 'w') as f:
        for i, point in enumerate(points):
            f.write(f"v {point[0]} {point[1]} {point[2]}\n")
        for i in range(len(points) - 1):
            f.write(f"l {i+1} {i+2}\n")

# Запуск анимации
plt.ion()  # Включение интерактивного режима
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-150, 150)
ax.set_ylim(-150, 150)
ax.set_zlim(-150, 150)

for i in range(100):
    points = update(ax)
    plt.pause(5)  # Пауза между кадрами
    plt.draw()  # Отрисовка текущего кадра

    # Сохраняем каждый кадр в файл OBJ
    filename = os.path.join(os.path.expanduser("~"), "Desktop", f"lomannaya_linia_{i+1}.obj")
    save_to_obj(points, filename)
    time.sleep(0.01)  # Пауза перед сохранением файла
    print(f"Model saved as {filename}")

plt.ioff()  # Выключение интерактивного режима
plt.show()  # Окончательный кадр
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def create_obj_file(vertex, edges, filename):
    """
    Создает OBJ-файл из заданных вершин и граней.

    :param vertex: Массив вершин в формате [(x, y, z),...]
    :param edges: Массив граней в формате [(v1, v2, v3),...], где v1, v2, v3 - индексы вершин
    :param filename: Имя файла OBJ
    """
    with open(filename, 'w') as f:
        # Записать вершины
        for i, v in enumerate(vertex):
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

        # Записать грани
        for edge in edges:
            f.write(f"f {edge[0] + 1} {edge[1] + 1} {edge[2] + 1}\n")

def generate_random_vertex(num_vertex, min_val, max_val):
    """
    Генерирует случайные вершины.

    :param num_vertex: Количество вершин
    :param min_val: Минимальное значение координаты
    :param max_val: Максимальное значение координаты
    :return: Список вершин в формате [(x, y, z),...]
    """
    return [(random.uniform(min_val, max_val), random.uniform(min_val, max_val), random.uniform(min_val, max_val)) for _ in range(num_vertex)]

def generate_random_edges(num_vertex, num_edges):
    """
    Генерирует случайные грани.

    :param num_vertex: Количество вершин
    :param num_edges: Количество граней
    :return: Список граней в формате [(v1, v2, v3),...]
    """
    edges = []
    for _ in range(num_edges):
        v1, v2, v3 = random.sample(range(num_vertex), 3)
        edges.append((v1, v2, v3))
    return edges

# Генерация случайных вершин и граней
num_vertex = random.randint(5, 20)
num_edges = random.randint(5, 20)
vertex = generate_random_vertex(num_vertex, -10, 10)
edges = generate_random_edges(num_vertex, num_edges)

# Сохранение модели в OBJ файл
desktop_path = os.path.expanduser("~")
filename = os.path.join(desktop_path, "Desktop", "random_model.obj")
create_obj_file(vertex, edges, filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def animate(frame):
    ax.clear()
    num_vertex = random.randint(5, 20)
    num_edges = random.randint(5, 20)
    vertex = generate_random_vertex(num_vertex, -10, 10)
    edges = generate_random_edges(num_vertex, num_edges)
    ax.scatter(*zip(*vertex), color='r', alpha=0.5)
    for edge in edges:
        ax.plot3D(*zip(vertex[edge[0]], vertex[edge[1]], vertex[edge[2]]), c='b')
ani = animation.FuncAnimation(fig, animate, frames=range(100), interval=100, repeat=True)
plt.show()
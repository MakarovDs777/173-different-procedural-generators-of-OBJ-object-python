import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

# Функция для генерации случайных самоподобий
def choose_random_shape(shapes, probabilities):
    return np.random.choice(shapes, p=probabilities)

def draw_shape(shape_type, center, size):
    vertices = []
    faces = []
    if shape_type == 0:  # Куб
        x, y, z = center
        half_size = size / 2
        # Вершины куба
        vertices = [
            [x - half_size, y - half_size, z - half_size],
            [x + half_size, y - half_size, z - half_size],
            [x + half_size, y + half_size, z - half_size],
            [x - half_size, y + half_size, z - half_size],
            [x - half_size, y - half_size, z + half_size],
            [x + half_size, y - half_size, z + half_size],
            [x + half_size, y + half_size, z + half_size],
            [x - half_size, y + half_size, z + half_size]
        ]
        # Грани куба (по 2 треугольника на каждую грань)
        faces = [
            [0, 1, 2], [0, 2, 3],  # Нижняя грань
            [4, 5, 6], [4, 6, 7],  # Верхняя грань
            [0, 1, 5], [0, 5, 4],  # Передняя грань
            [1, 2, 6], [1, 6, 5],  # Правая грань
            [2, 3, 7], [2, 7, 6],  # Задняя грань
            [3, 0, 4], [3, 4, 7]   # Левая грань
        ]
    elif shape_type == 1:  # Шар
        phi, theta = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x = center[0] + size * np.outer(np.cos(phi), np.sin(theta))
        y = center[1] + size * np.outer(np.sin(phi), np.sin(theta))
        z = center[2] + size * np.outer(np.ones(np.size(phi)), np.cos(theta))
        vertices = np.c_[x.flatten(), y.flatten(), z.flatten()]
        faces = []  # Треугольники не определяются для шара простым способом
        for i in range(len(theta) - 1):
            for j in range(len(phi) - 1):
                a = i * len(phi) + j
                b = a + len(phi)
                c = a + 1
                d = b + 1
                faces.append([a, c, b])
                faces.append([c, d, b])

    elif shape_type == 2:  # Ромб
        x, y, z = center
        vertices = [
            [x, y + size / 2, z], 
            [x, y - size / 2, z],
            [x + size / 2, y, z], 
            [x - size / 2, y, z]
        ]
        faces = [[0, 1, 2], [1, 3, 2]]  # Два треугольника образуют ромб

    return np.array(vertices), faces

def draw_super_fractal(x, y, z, length, min_length, points, meshes, shapes, probabilities, depth):
    if length > min_length and depth < 5:
        shape_type = choose_random_shape(shapes, probabilities)
        vertices, faces = draw_shape(shape_type, (x, y, z), length)

        # Обновление индексов вершин
        index_offset = len(points)
        points.extend(vertices)  # Объединяем все вершины
        for face in faces:
            meshes.append([idx + index_offset for idx in face])  # Сдвигаем индексы

        # Случайные углы и длины для создания сложности
        for angle in np.linspace(-np.pi / 4, np.pi / 4, num=3):
            new_length = length * np.random.uniform(0.4, 0.8)  # Случайное изменение длины
            draw_super_fractal(
                x + new_length * np.cos(angle),
                y + new_length * np.sin(angle),
                z,
                new_length,
                min_length,
                points,
                meshes,
                shapes,
                probabilities,
                depth + 1
            )

# Функция для сохранения фрактала
def save_fractal(points, meshes, filename):
    # Сохраняем в формате .obj
    with open(filename, 'w') as f:
        for v in points:
            f.write('v {:.6f} {:.6f} {:.6f}\n'.format(v[0], v[1], v[2]))
        for face in meshes:
            f.write('f {} {} {}\n'.format(face[0] + 1, face[1] + 1, face[2] + 1))  # .obj начинается с 1

    print(f"Модель сохранена как {filename}")

# Начальные параметры
x, y, z = 64, 64, 64  # Центрирование фрактала
length = 20  # Начальная длина
min_length = 1
shapes = [0, 1, 2]  # Куб, шар, ромб
probabilities = [0.3, 0.4, 0.3]  # вероятности выбора

points = []
meshes = []
draw_super_fractal(x, y, z, length, min_length, points, meshes, shapes, probabilities, depth=0)

# Преобразование точек в массив
points = np.array(points)

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Создание меша
poly3d = Poly3DCollection(points[meshes], alpha=0.5, edgecolor='k')
ax.add_collection3d(poly3d)

# Настройки отображения
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.auto_scale_xyz([0, 128], [0, 128], [0, 128])
plt.show()

# Сохранение фрактала в формате OBJ на Рабочий стол
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
output_path = os.path.join(desktop_path, 'fractal.obj')
save_fractal(points, meshes, output_path)

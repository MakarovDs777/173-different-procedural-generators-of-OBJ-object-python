import numpy as np
import os
from scipy.spatial import Delaunay

# Функция для генерации случайных самоподобий
def choose_random_shape(shapes, probabilities):
    return np.random.choice(shapes, p=probabilities)

def draw_shape(points, shape_type, center, size):
    if shape_type == 0:  # квадрат
        x, y, z = center
        half_size = size / 2
        for dx in np.linspace(-half_size, half_size, num=5):
            for dy in np.linspace(-half_size, half_size, num=5):
                for dz in np.linspace(-half_size, half_size, num=5):
                    points.append([x + dx, y + dy, z + dz])
    elif shape_type == 1:  # шар
        phi, theta = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x = center[0] + size * np.outer(np.cos(phi), np.sin(theta))
        y = center[1] + size * np.outer(np.sin(phi), np.sin(theta))
        z = center[2] + size * np.outer(np.ones(np.size(phi)), np.cos(theta))
        points.extend(np.c_[x.flatten(), y.flatten(), z.flatten()])
    elif shape_type == 2:  # ромб
        x, y, z = center
        points.extend([[x, y + size / 2, z], [x, y - size / 2, z],
                       [x + size / 2, y, z], [x - size / 2, y, z]])

def draw_super_fractal(x, y, z, length, min_length, points, shapes, probabilities, depth):
    if length > min_length and depth < 5:
        shape_type = choose_random_shape(shapes, probabilities)
        draw_shape(points, shape_type, (x, y, z), length)

        for angle in np.linspace(-np.pi / 4, np.pi / 4, num=3):
            new_length = length * np.random.uniform(0.3, 0.7)
            new_x = x + length * np.cos(angle) * np.random.uniform(0.5, 1.5)
            new_y = y + length * np.sin(angle) * np.random.uniform(0.5, 1.5)
            draw_super_fractal(new_x, new_y, z, new_length, min_length, points, shapes, probabilities, depth + 1)

def save_mesh_as_obj(points, faces, filename):
    with open(filename, 'w') as f:
        for v in points:
            f.write('v {:.6f} {:.6f} {:.6f}\n'.format(v[0], v[1], v[2]))
        for face in faces:
            f.write('f {} {} {}\n'.format(face[0] + 1, face[1] + 1, face[2] + 1))

# Начальные параметры
x, y, z = 64, 64, 64
length = 20
min_length = 1
shapes = [0, 1, 2]  # квадрат, шар, ромб
probabilities = [0.3, 0.4, 0.3]

points = []
draw_super_fractal(x, y, z, length, min_length, points, shapes, probabilities, depth=0)

# Преобразование точек в массив
points = np.array(points)

# Выполнение триангуляции
tri = Delaunay(points[:, :2])  # Используем только X и Y для 2D триангуляции
faces = tri.simplices  # Получение индексов вершин для треугольников

# Сохранение меша в формате OBJ на Рабочий стол
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
output_path = os.path.join(desktop_path, 'super_fractal_mesh.obj')
save_mesh_as_obj(points, faces, output_path)
print(f"Модель сохранена как {output_path}")
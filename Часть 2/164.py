import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
import os

# Функция для генерации случайных самоподобий
def choose_random_shape(shapes, probabilities):
    return np.random.choice(shapes, p=probabilities)

def create_surface_from_points(points, grid_size):
    array = np.zeros(grid_size, dtype=bool)

    for point in points:
        idx = np.floor(point).astype(int)
        if np.all(idx >= 0) and np.all(idx < np.array(grid_size)):
            array[tuple(idx)] = 1

    return array

# Функция для генерации фигур с большей плотностью
def draw_shape(points, shape_type, center, size):
    if shape_type == 0:  # квадрат
        x, y, z = center
        half_size = size / 2
        for dx in np.linspace(-half_size, half_size, num=5):  # Увеличено количество точек
            for dy in np.linspace(-half_size, half_size, num=5):
                for dz in np.linspace(-half_size, half_size, num=5):
                    points.append([x + dx, y + dy, z + dz])
    elif shape_type == 1:  # шар
        phi, theta = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]  # Увеличено количество полярных углов
        x = center[0] + size * np.outer(np.cos(phi), np.sin(theta))
        y = center[1] + size * np.outer(np.sin(phi), np.sin(theta))
        z = center[2] + size * np.outer(np.ones(np.size(phi)), np.cos(theta))
        points.extend(np.c_[x.flatten(), y.flatten(), z.flatten()])
    elif shape_type == 2:  # ромб
        x, y, z = center
        points.extend([[x, y + size / 2, z], [x, y - size / 2, z],
                       [x + size / 2, y, z], [x - size / 2, y, z]])

def draw_fractal_makarov(x, y, z, length, min_length, points, shapes, probabilities, depth):
    if length > min_length and depth < 5:  # Увеличенная глубина рекурсии
        shape_type = choose_random_shape(shapes, probabilities)
        draw_shape(points, shape_type, (x, y, z), length)

        for angle in np.linspace(-np.pi / 4, np.pi / 4, num=3):  # Увеличенное количество углов для большей плотности
            draw_fractal_makarov(x + length * np.cos(angle), 
                                  y + length * np.sin(angle), 
                                  z, length * 0.5, min_length, points, shapes, probabilities, depth + 1)

def save_fractal(verts, faces, filename):
    with open(filename, 'w') as f:
        for v in verts:
            f.write('v {:.6f} {:.6f} {:.6f}\n'.format(v[0], v[1], v[2]))
        for face in faces:
            f.write('f {} {} {}\n'.format(face[0]+1, face[1]+1, face[2]+1))

# Начальные параметры
x, y, z = 64, 64, 64  # Центрирование фрактала
length = 20  # Начальная длина
min_length = 1
shapes = [0, 1, 2]  # квадрат, шар, ромб
probabilities = [0.3, 0.4, 0.3]  # вероятности выбора

points = []
draw_fractal_makarov(x, y, z, length, min_length, points, shapes, probabilities, depth=0)

# Преобразование точек в массив
points = np.array(points)
grid_size = (128, 128, 128)
scaled_points = (points - np.min(points, axis=0)) / (np.max(points, axis=0) - np.min(points, axis=0)) * grid_size[0]
scaled_points = np.clip(scaled_points, 0, np.array(grid_size) - 1)

# Создаем 3D массив на основе масштабированных точек
array = create_surface_from_points(scaled_points, grid_size)

# Создание изосурфейса для всех линий фрактала
verts, faces, _, _ = measure.marching_cubes(array, level=0.5)

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
verts -= np.min(verts, axis=0)  # Центрируем модель
poly3d = Poly3DCollection(verts[faces], alpha=0.5, edgecolor='k')
ax.add_collection3d(poly3d)

# Настройки отображения
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.auto_scale_xyz([0, grid_size[0]], [0, grid_size[1]], [0, grid_size[2]])
plt.show()

# Сохранение фрактала в формате OBJ на Рабочий стол
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
output_path = os.path.join(desktop_path, 'fractal.obj')
save_fractal(verts, faces, output_path)
print(f"Модель сохранена как {output_path}")
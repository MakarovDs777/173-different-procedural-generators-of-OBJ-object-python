import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
import os

def generate_space():
    x, y, z = np.random.uniform(-10, 10), np.random.uniform(-10, 10), np.random.uniform(-10, 10)
    depth = np.random.randint(1, 10)
    points = [np.array([x, y, z])]
    for i in range(depth):
        x1 = x + np.random.uniform(-1, 1)
        y1 = y + np.random.uniform(-1, 1)
        z1 = z + np.random.uniform(-1, 1)
        points.append(np.array([x1, y1, z1]))
    return points

def create_surface_from_points(points, grid_size):
    array = np.zeros(grid_size, dtype=bool)
    for point in points:
        idx = np.floor(point).astype(int)
        if np.all(idx >= 0) and np.all(idx < np.array(grid_size)):
            array[tuple(idx)] = 1
    return array

def save_fractal(verts, faces, filename):
    try:
        with open(filename, 'w') as f:
            for v in verts:
                f.write('v {:.6f} {:.6f} {:.6f}\n'.format(v[0], v[1], v[2]))
            for face in faces:
                f.write('f {} {} {}\n'.format(face[0]+1, face[1]+1, face[2]+1))
        print(f"Model saved as {filename}")
    except Exception as e:
        print(f"Error saving model: {e}")

# Начальные параметры
points = []
for i in range(100):
    points.extend(generate_space())

# Масштабируем точки так, чтобы они вмещались в массив
points = np.array(points)
min_vals = np.min(points, axis=0)
max_vals = np.max(points, axis=0)
scale_factors = np.array((128, 128, 128)) / (max_vals - min_vals)
scaled_points = (points - min_vals) * scale_factors
scaled_points = np.clip(scaled_points, 0, np.array((128, 128, 128)) - 1)

# Создаем 3D массив на основе масштабированных точек
array = create_surface_from_points(scaled_points, (128, 128, 128))

# Создание изосурфейса для всех линий фрактала
verts, faces, _, _ = measure.marching_cubes(array, level=0.5)

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Визуализация модели
verts = verts * np.array((128, 128, 128)) / np.max(np.array((128, 128, 128)))  # Масштабируем обратно для визуализации
verts -= np.min(verts, axis=0)  # Центрируем модель

# Создаем коллекцию полигонов для визуализации
poly3d = Poly3DCollection(verts[faces], alpha=0.5, edgecolor='k')
ax.add_collection3d(poly3d)

# Настройки отображения
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.auto_scale_xyz([0, 1], [0, 1], [0, 1])  # Устанавливаем диапазоны для осей

# Показываем окно с моделью
plt.show()

# Сохранение фрактала в формате OBJ
output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'fractal.obj')
save_fractal(verts, faces, output_path)
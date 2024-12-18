import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os

def create_hole(position, size):
    """Создает куб в форме отверстия"""
    hole = trimesh.creation.box(extents=size)
    hole.apply_translation(position)
    return hole

def generate_cube_with_holes():
    # Создание куба
    cube = trimesh.creation.box(extents=(2, 2, 2))

    # Размеры отверстия для столбов
    hole_size = [1.0, 1.0, 2.0]  # Столбы вдоль оси Z
    hole_size_x = [2.0, 1.0, 1.0]  # Столбы вдоль оси X
    hole_size_y = [1.0, 2.0, 1.0]  # Столбы вдоль оси Y

    # Определяем позиции для столбов по оси Z
    hole_positions_z = [
        [0, 0, -1],  # столб вниз
        [0, 0, 1],   # столб вверх
        [0, 0, 0],   # центральный столб вдоль Z
        [0, 0, 0],    # центральный по Z (заменить для правильного вертикального вычитания)
    ]

    # Определяем позиции для столбов по оси X
    hole_positions_x = [
        [-1, 0, 0],  # столб слева
        [1, 0, 0],   # столб справа
        [0, 0, 0],   # центральный столб вдоль X
        [0, 0, 0],    # замена для центрального вычитания
    ]

    # Определяем позиции для столбов по оси Y
    hole_positions_y = [
        [0, -1, 0],  # столб сзади
        [0, 1, 0],   # столб спереди
        [0, 0, 0],   # центральный столб вдоль Y
        [0, 0, 0],    # замена для центрального вычитания
    ]

    # Создание и вычитание столбов по оси Z
    for pos in hole_positions_z:
        hole = create_hole(pos, hole_size)
        cube = cube.difference(hole)

    # Создание и вычитание столбов по оси X
    for pos in hole_positions_x:
        hole = create_hole(pos, hole_size_x)
        cube = cube.difference(hole)

    # Создание и вычитание столбов по оси Y
    for pos in hole_positions_y:
        hole = create_hole(pos, hole_size_y)
        cube = cube.difference(hole)

    return cube

# Генерация куба с отверстиями
mesh = generate_cube_with_holes()

# Сохранение куба в OBJ файл
desktop_path = os.path.expanduser("~")
filename = os.path.join(desktop_path, "Desktop", "cube_with_holes.obj")
mesh.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], color='r', alpha=0.5)
plt.show()
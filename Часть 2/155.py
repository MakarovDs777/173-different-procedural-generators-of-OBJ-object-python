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

    # Размеры отверстия
    hole_size_x = [2.0, 1.0, 1.0]  # Отверстия по оси X

    # Определяем позиции для столбов по X (по одному слева и справа)
    hole_positions_x = [
        [-1 + hole_size_x[0] / 2, 0, 0],  # столб слева
        [1 - hole_size_x[0] / 2, 0, 0],   # столб справа
    ]

    # Создание и вычитание столбов по оси X
    for pos in hole_positions_x:
        hole = create_hole(pos, hole_size_x)
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

import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os

def create_hole(position, size):
    """Создаёт куб в форме отверстия."""
    hole = trimesh.creation.box(extents=size)
    hole.apply_translation(position)
    return hole

def generate_cube_with_connected_holes():
    # Создание основного куба
    cube = trimesh.creation.box(extents=(2, 2, 2))

    # Размеры отверстий
    hole_size = [1.0, 1.0, 0.2]  # Отверстие 1.0x1.0 и глубина 0.2
    channel_size = [0.2, 0.2, 2.0]  # Канал, который соединяет отверстия

    # Определяем позиции для отверстий
    hole_positions = [
        [0, 0, -1 + hole_size[2] / 2],  # нижняя грань
        [0, 0, 1 - hole_size[2] / 2],   # верхняя грань
        [-1 + hole_size[0] / 2, 0, 0],  # левая грань
        [1 - hole_size[0] / 2, 0, 0],   # правая грань
        [0, -1 + hole_size[1] / 2, 0],  # задняя грань
        [0, 1 - hole_size[1] / 2, 0]    # передняя грань
    ]

    # Вычитание отверстий из куба
    for pos in hole_positions:
        hole = create_hole(pos, hole_size)
        cube = cube.difference(hole)

    # Определяем позиции для каналов, чтобы соединить отверстия
    channel_positions = [
        [0, 0, -0.1],  # канал между верхним и нижним отверстиями
        [0, 0, 0],     # центральный канал
        [-1 + hole_size[0] / 2, 0, 0],  # канал соединения через левую грань
        [1 - hole_size[0] / 2, 0, 0],   # канал соединения через правую грань
        [0, -1 + hole_size[1] / 2, 0],  # канал соединения через заднюю грань
        [0, 1 - hole_size[1] / 2, 0]    # канал соединения через переднюю грань
    ]

    # Создание каналов
    for pos in channel_positions:
        channel = create_hole(pos, channel_size)
        cube = cube.difference(channel)

    return cube

# Генерация куба с соединёнными отверстиями
mesh = generate_cube_with_connected_holes()

# Сохранение куба в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "cube_with_connected_holes.obj")
mesh.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], color='r', alpha=0.5)
ax.set_title("Cube with Connected Holes")
plt.show()

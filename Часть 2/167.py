import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os

def create_hole(position, size):
    """Создает куб в форме отверстия."""
    hole = trimesh.creation.box(extents=size)
    hole.apply_translation(position)
    return hole

def generate_cube_with_corridor_and_room():
    # Создание куба
    cube = trimesh.creation.box(extents=(12, 4, 12))

    # Размеры коридора
    corridor_size = (1.0, 1.0, 1.0)  # Размеры коридора по осям (X, Y, Z)

    # Определяем позицию коридора
    corridor_position = [1, 2, -8]  # Коридор идет вверх

    # Создание коридора и вычитание из куба
    corridor = create_hole(corridor_position, corridor_size)
    cube = cube.difference(corridor)

    # Генерация комнаты, которая будет соединяться с коридором
    room = trimesh.creation.box(extents=(30, 2, 1.5))  # Размеры комнаты
    room_position = [10.0, -1.0, 0.0]  # Позиция комнаты (размещаем над кубом)
    room.apply_translation(room_position)

    # Объединение куба и комнаты
    combined_mesh = cube.union(room)

    return combined_mesh

# Генерация куба с коридором и комнатой
mesh = generate_cube_with_corridor_and_room()

# Сохранение модели в OBJ файл
desktop_path = os.path.expanduser("~")
filename = os.path.join(desktop_path, "Desktop", "cube_with_corridor_and_room.obj")
mesh.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], color='r', alpha=0.5)
plt.show()
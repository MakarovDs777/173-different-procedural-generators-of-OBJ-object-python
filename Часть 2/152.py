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
    ]

    # Определяем позиции для столбов по оси X
    hole_positions_x = [
        [-1, 0, 0],  # столб слева
        [1, 0, 0],   # столб справа
        [0, 0, 0],   # центральный столб вдоль X
    ]

    # Определяем позиции для столбов по оси Y
    hole_positions_y = [
        [0, -1, 0],  # столб сзади
        [0, 1, 0],   # столб спереди
        [0, 0, 0],   # центральный столб вдоль Y
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

    # Удаление угловых вершин
    corner_vertices = np.array([
        [-1, -1, -1],
        [-1, -1,  1],
        [-1,  1, -1],
        [-1,  1,  1],
        [ 1, -1, -1],
        [ 1, -1,  1],
        [ 1,  1, -1],
        [ 1,  1,  1],
    ])

    # Находим индексы угловых вершин в массиве вершин куба
    keep_indices = []
    for index, vertex in enumerate(cube.vertices):
        if not any(np.all(vertex == corner) for corner in corner_vertices):
            keep_indices.append(index)

    # Создаем новый массив вершин без угловых вершин
    new_vertices = cube.vertices[keep_indices]

    # Создаем новый массив граней, связывая старые индексы с новыми
    old_to_new_index = {old_index: new_index for new_index, old_index in enumerate(keep_indices)}
    new_faces = []
    for face in cube.faces:
        if all(vertex in old_to_new_index for vertex in face):
            new_face = [old_to_new_index[vertex] for vertex in face]
            new_faces.append(new_face)

    # Создаем новый объект Trimesh
    new_mesh = trimesh.Trimesh(vertices=new_vertices, faces=new_faces)

    return new_mesh

# Генерация куба с отверстиями и без угловых вершин
mesh = generate_cube_with_holes()

# Сохранение куба в OBJ файл
desktop_path = os.path.expanduser("~")
filename = os.path.join(desktop_path, "Desktop", "cube_with_holes_no_corners.obj")
mesh.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], color='r', alpha=0.5)
plt.show()
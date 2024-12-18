import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

# Функция для генерации 2D-поля с коридорами
def generate_field(shape):
    array = np.zeros(shape, dtype=float)

    # Генерация точек для коридоров
    points = []
    for _ in range(10):
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        points.append([x, y])  # Генерируем точки

    # Генерация коридоров между точками
    for i in range(len(points) - 1):
        start_point = points[i]
        end_point = points[i + 1]

        # Горизонтальный или вертикальный коридор
        if abs(start_point[0] - end_point[0]) > abs(start_point[1] - end_point[1]):
            for new_x in range(min(start_point[0], end_point[0]), max(start_point[0], end_point[0]) + 1):
                new_y = start_point[1]
                array[new_x, new_y] = 1.0
                # Делаем коридоры более жирными
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        x1, y1 = new_x + k, new_y + l
                        if 0 <= x1 < shape[0] and 0 <= y1 < shape[1]:
                            array[x1, y1] = 1.0
        else:
            for new_y in range(min(start_point[1], end_point[1]), max(start_point[1], end_point[1]) + 1):
                new_x = start_point[0]
                array[new_x, new_y] = 1.0
                # Делаем коридоры более жирными
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        x1, y1 = new_x + k, new_y + l
                        if 0 <= x1 < shape[0] and 0 <= y1 < shape[1]:
                            array[x1, y1] = 1.0

    return array

# Функция для генерации комнаты
def generate_room(x, y):
    room_size = np.random.randint(5, 15)
    room_height = np.random.randint(5, 10)
    vertices = np.array([
        [0, 0, 0],
        [room_size, 0, 0],
        [room_size, room_size, 0],
        [0, room_size, 0],
        [0, 0, room_height],
        [room_size, 0, room_height],
        [room_size, room_size, room_height],
        [0, room_size, room_height]
    ])
    faces = np.array([
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7]
    ])
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.vertices += [x, y, 0]
    return mesh

# Параметры
shape = (128, 128)  # Размеры 2D массива

# Генерация 2D-поля с коридорами
field = generate_field(shape)

# Создание изосурфейса
contours = measure.find_contours(field, 0.5)

# Создание mesh с острыми углами
corridor_mesh = trimesh.Trimesh(vertices=None, faces=None)
for contour in contours:
    contour = contour.astype(int)
    contour = np.column_stack((contour[:, 0], contour[:, 1], np.zeros(contour.shape[0])))
    vertices = np.zeros((contour.shape[0] * 2, 3))
    for i in range(contour.shape[0]):
        vertices[i * 2] = contour[i]
        vertices[i * 2 + 1] = contour[i] + np.array([0, 0, 1])
    faces = np.zeros((contour.shape[0] * 4, 3), dtype=int)
    for i in range(contour.shape[0]):
        faces[i * 4] = [i * 2, (i + 1) % (contour.shape[0] * 2), i * 2 + 1]
        faces[i * 4 + 1] = [(i + 1) % (contour.shape[0] * 2), (i + 1) % (contour.shape[0] * 2) + 1, i * 2 + 1]
        faces[i * 4 + 2] = [i * 2, i * 2 + 1, (i + 1) % (contour.shape[0] * 2)]
        faces[i * 4 + 3] = [(i + 1) % (contour.shape[0] * 2), (i + 1) % (contour.shape[0] * 2) + 1, i * 2]
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    corridor_mesh = trimesh.util.concatenate([corridor_mesh, mesh])

# Генерация комнат
rooms = []
for _ in range(10):
    x = np.random.randint(10, 128 - 10)
    y = np.random.randint(10, 128 - 10)
    room = generate_room(x, y)
    rooms.append(room)

# Объединение комнат и коридоров
meshes = [corridor_mesh] + rooms
mesh = trimesh.util.concatenate(meshes)

# Сохранение mesh на рабочий стол
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "mesh.stl")
mesh.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], color='r', alpha=0.5)
plt.show()

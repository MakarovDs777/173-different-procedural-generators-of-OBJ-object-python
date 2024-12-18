import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os

# Функция для генерации 3D-поля с ровными коридорами
def generate_delaunay_field(shape):
    points = []
    for _ in range(10):
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        points.append([x, y, shape[2] // 2])  # Генерация точек на фиксированной высоте

    meshes = []

    # Создание кубов на фиксированной высоте
    for i in range(len(points) - 1):
        dx = points[i+1][0] - points[i][0]
        dy = points[i+1][1] - points[i][1]
        length = max(abs(dx), abs(dy))

        if abs(dx) > abs(dy):
            for j in range(length + 1):
                new_x = int(points[i][0] + j * dx // length)
                new_y = points[i][1]
                new_z = int(points[i][2])
                size = 2
                box = trimesh.primitives.Box(extents=(size, size, size), transform=trimesh.transformations.translation_matrix([new_x, new_y, new_z]))
                meshes.append(box)
        else:
            for j in range(length + 1):
                new_x = points[i][0]
                new_y = int(points[i][1] + j * dy // length)
                new_z = int(points[i][2])
                size = 2
                box = trimesh.primitives.Box(extents=(size, size, size), transform=trimesh.transformations.translation_matrix([new_x, new_y, new_z]))
                meshes.append(box)

    # Объединение всех кубов в одну сетку
    mesh = trimesh.util.concatenate(meshes)
    return mesh

# Параметры
shape = (128, 128, 128)

# Генерация 3D-поля с коридорами
delaunay_field = generate_delaunay_field(shape)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "delaunay.obj")
delaunay_field.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(delaunay_field.vertices[:, 0], delaunay_field.vertices[:, 1], delaunay_field.vertices[:, 2], color='r', alpha=0.5)
for face in delaunay_field.faces:
    v1, v2, v3 = delaunay_field.vertices[face]
    ax.plot3D([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], 'r', alpha=0.5)
    ax.plot3D([v2[0], v3[0]], [v2[1], v3[1]], [v2[2], v3[2]], 'r', alpha=0.5)
    ax.plot3D([v3[0], v1[0]], [v3[1], v1[1]], [v3[2], v1[2]], 'r', alpha=0.5)
plt.show()

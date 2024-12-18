import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from scipy.spatial import Delaunay
import os

# Функция для генерации 3D-поля с триангуляцией Делоне
def generate_delaunay_field(shape):
    array = np.zeros(shape, dtype=float)
    points = []
    for i in range(100):
        x = np.random.uniform(0, shape[0])
        y = np.random.uniform(0, shape[1])
        z = np.random.uniform(0, shape[2])
        points.append([x, y, z])

    # Преобразование точек в NumPy массив 
    points = np.array(points)

    # Выполнить триангуляцию Делоне
    triangulation = Delaunay(points)

    # Постройте график треугольников
    for triangle in triangulation.simplices:
        for i in range(3):
            dx = points[triangle[(i+1)%3], 0] - points[triangle[i], 0]
            dy = points[triangle[(i+1)%3], 1] - points[triangle[i], 1]
            dz = points[triangle[(i+1)%3], 2] - points[triangle[i], 2]
            length = int(np.sqrt(dx**2 + dy**2 + dz**2))
            for j in range(length):
                new_x = int(points[triangle[i], 0] + j * dx // length)
                new_y = int(points[triangle[i], 1] + j * dy // length)
                new_z = int(points[triangle[i], 2] + j * dz // length)
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    # Делаем линии более жирными
                    if new_x > 0:
                        array[new_x-1, new_y, new_z] = 1.0
                    if new_x < shape[0] - 1:
                        array[new_x+1, new_y, new_z] = 1.0
                    if new_y > 0:
                        array[new_x, new_y-1, new_z] = 1.0
                    if new_y < shape[1] - 1:
                        array[new_x, new_y+1, new_z] = 1.0
                    if new_z > 0:
                        array[new_x, new_y, new_z-1] = 1.0
                    if new_z < shape[2] - 1:
                        array[new_x, new_y, new_z+1] = 1.0
    return array

def generate_cube_field(shape):
    array = np.ones(shape, dtype=float)
    # Удаляем все 6 сторон куба
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                if x == 0 or x == shape[0] - 1 or y == 0 or y == shape[1] - 1 or z == 0 or z == shape[2] - 1:
                    array[x, y, z] = 0.0
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива

# Генерация 3D-поля с триангуляцией Делоне
delaunay_field = generate_delaunay_field(shape)

# Генерация 3D-поля с кубом
cube_field = generate_cube_field(shape)

# Объединение полей логическим оператором "или"
field = np.logical_and(delaunay_field, cube_field).astype(float)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "delaunay.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)
plt.show()


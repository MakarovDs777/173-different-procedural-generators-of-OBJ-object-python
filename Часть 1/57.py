import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os
from scipy.interpolate import interp1d

def generate_hair_field(shape, num_hairs, hair_length, hair_radius):
    array = np.zeros(shape, dtype=float)
    for _ in range(num_hairs):
        x, y, z = np.random.randint(0, shape[0]), np.random.randint(0, shape[1]), np.random.randint(0, shape[2])
        for _ in range(hair_length):
            dx = np.random.randint(-1, 2)
            dy = np.random.randint(-1, 2)
            dz = np.random.randint(1, 3)
            x += dx
            y += dy
            z += dz
            if 0 <= x < shape[0] and 0 <= y < shape[1] and 0 <= z < shape[2]:
                array[x, y, z] = 1.0
                # Делаем волосы более жирными
                if x > 0:
                    array[x-1, y, z] = 1.0
                if x < shape[0] - 1:
                    array[x+1, y, z] = 1.0
                if y > 0:
                    array[x, y-1, z] = 1.0
                if y < shape[1] - 1:
                    array[x, y+1, z] = 1.0
                if z > 0:
                    array[x, y, z-1] = 1.0
                if z < shape[2] - 1:
                    array[x, y, z+1] = 1.0
    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
num_hairs = 100  # Количество волос
hair_length = 20  # Длина волос
hair_radius = 1  # Радиус волос

# Генерация 3D-поля с волосами
hair_field = generate_hair_field(shape, num_hairs, hair_length, hair_radius)

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

points = []
for i in range(shape[0]):
    for j in range(shape[1]):
        for k in range(shape[2]):
            if hair_field[i, j, k] == 1.0:
                points.append([i, j, k])

# Интерполяция
t = np.linspace(0, 1, len(points))
x = np.array([point[0] for point in points])
y = np.array([point[1] for point in points])
z = np.array([point[2] for point in points])

x_interp = interp1d(t, x, kind='cubic')
y_interp = interp1d(t, y, kind='cubic')
z_interp = interp1d(t, z, kind='cubic')

t_interp = np.linspace(0, 1, 1000)
x_interp = x_interp(t_interp)
y_interp = y_interp(t_interp)
z_interp = z_interp(t_interp)

ax.plot(x_interp, y_interp, z_interp, 'b-')

ax.scatter(*zip(*points))

# Генерация трубок
radius = 1.0
theta = np.linspace(0, 2*np.pi, 100)

tube_x = []
tube_y = []
tube_z = []

for i in range(num_hairs):
    x_hair = np.array([point[0] for point in points if point[2] == i])
    y_hair = np.array([point[1] for point in points if point[2] == i])
    z_hair = np.array([point[2] for point in points if point[2] == i])

    if len(x_hair) < 4:
        continue

    x_hair_interp = interp1d(np.linspace(0, 1, len(x_hair)), x_hair, kind='linear')
    y_hair_interp = interp1d(np.linspace(0, 1, len(y_hair)), y_hair, kind='linear')
    z_hair_interp = interp1d(np.linspace(0, 1, len(z_hair)), z_hair, kind='linear')

    t_hair_interp = np.linspace(0, 1, 100)
    x_hair_interp = x_hair_interp(t_hair_interp)
    y_hair_interp = y_hair_interp(t_hair_interp)
    z_hair_interp = z_hair_interp(t_hair_interp)

    for j in range(len(x_hair_interp)):
        for k in range(len(theta)):
            tube_x.append(x_hair_interp[j] + radius * np.cos(theta[k]))
            tube_y.append(y_hair_interp[j] + radius * np.sin(theta[k]))
            tube_z.append(z_hair_interp[j])

# Создание вершин и треугольников для меша
vertices = []
faces = []

tube_idx = 0
for i in range(len(x_hair_interp) - 1):
    for j in range(num_hairs):
        tube_x_section = []
        tube_y_section = []
        tube_z_section = []
        for k in range(len(theta)):
            if tube_idx + k < len(tube_x):
                tube_x_section.append(tube_x[tube_idx + k])
                tube_y_section.append(tube_y[tube_idx + k])
                tube_z_section.append(tube_z[tube_idx + k])
        tube_idx += len(theta)

        for k in range(len(theta) - 1):
            if tube_idx - len(theta) + k < len(tube_x) and tube_idx - len(theta) + k + 1 < len(tube_x) and tube_idx - len(theta) + k + len(theta) < len(tube_x) and tube_idx - len(theta) + k + len(theta) + 1 < len(tube_x):
                vertices.append([tube_x[tube_idx - len(theta) + k], tube_y[tube_idx - len(theta) + k], tube_z[tube_idx - len(theta) + k]])
                vertices.append([tube_x[tube_idx - len(theta) + k + 1], tube_y[tube_idx - len(theta) + k + 1], tube_z[tube_idx - len(theta) + k + 1]])
                vertices.append([tube_x[tube_idx - len(theta) + k], tube_y[tube_idx - len(theta) + k], tube_z[tube_idx - len(theta) + k] + 1])
                vertices.append([tube_x[tube_idx - len(theta) + k + 1], tube_y[tube_idx - len(theta) + k + 1], tube_z[tube_idx - len(theta) + k + 1] + 1])

                faces.append([tube_idx - len(theta) + k, tube_idx - len(theta) + k + 1, tube_idx - len(theta) + k + len(theta)])
                faces.append([tube_idx - len(theta) + k + 1, tube_idx - len(theta) + k + len(theta), tube_idx - len(theta) + k + len(theta) + 1])

# Сохранение меша в файл
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "tubes.obj")
with open(filename, "w") as f:
    for i, vertex in enumerate(vertices):
        f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
    for face in faces:
        f.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")
print(f"Tubes saved as {filename}")

# Визуализация меша
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

mesh = Poly3DCollection(vertices, facecolors='b', alpha=0.5)
ax.add_collection3d(mesh)

plt.show()
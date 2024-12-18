import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure

# Функция для генерации 3D поля
def generate_field(shape):
    field = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                field[i, j, k] = np.random.uniform(-1, 1)
    return field

# Функция для отрисовки изосурфейса
def draw_isosurface(field, level):
    verts, faces, _, _ = measure.marching_cubes(field, level=level)
    return verts, faces

# Функция для сохранения изосурфейса в файл OBJ
def save_to_obj(verts, faces, filename):
    with open(filename, 'w') as f:
        for i, vert in enumerate(verts):
            f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
        for i, face in enumerate(faces):
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

# Генерация 3D поля
field = generate_field((100, 100, 100))

# Отрисовка изосурфейса
verts, faces = draw_isosurface(field, level=0.0)

# Сохранение изосурфейса в файл OBJ который сохраняется в C:\Users\Ваш компьютер
filename = "isosurface.obj"
save_to_obj(verts, faces, filename)

# Отрисовка изосурфейса в 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], cmap='viridis', edgecolor='none')
plt.show()
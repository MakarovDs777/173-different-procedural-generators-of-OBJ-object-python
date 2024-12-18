import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_surface(image_path, shape):
    # Чтение изображения
    image = np.array(plt.imread(image_path))

    # Преобразование изображения в черно-белое
    image_gray = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])

    # Создаем 3D массив для поверхности
    surface = np.zeros(shape, dtype=float)

    # Генерируем поверхность на основе изображения
    for x in range(shape[0]):
        for y in range(shape[1]):
            pixel_value = image_gray[x, y]
            height = 1.0 - pixel_value  # чем темнее пиксель, тем выше бугор
            surface[x, y, int(height * shape[2])] = 1.0

    return surface

def save_surface_to_obj(surface, filename):
    # Создание изосурфейса
    verts, faces, _, _ = measure.marching_cubes(surface, level=0.5)

    # Сохранение изосурфейса в OBJ файл
    with open(filename, "w") as f:
        for j, vert in enumerate(verts):
            f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

def visualize_surface(surface):
    # Создание изосурфейса
    verts, faces, _, _ = measure.marching_cubes(surface, level=0.5)

    # Визуализация
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)
    plt.show()

# Параметры
image_path = r"Путь к файлу"
shape = (64, 64, 64)  # Размеры 3D массива
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "surface.obj")

# Генерация поверхности
surface = generate_surface(image_path, shape)

# Сохранение поверхности в OBJ файл
save_surface_to_obj(surface, filename)

# Визуализация поверхности
visualize_surface(surface)

print(f"Model saved as {filename}")
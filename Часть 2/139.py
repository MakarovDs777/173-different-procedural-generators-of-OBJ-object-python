import numpy as np
from scipy import ndimage
from skimage import measure
import os

# Генерация синтвейв-шума
def generate_syntwave_noise(shape, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
    noise_map = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                x = i - shape[0] // 2
                y = j - shape[1] // 2
                z = k - shape[2] // 2
                r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
                noise_map[i, j, k] = np.sin(r / scale)
    return noise_map

# Основной цикл
shape = (128, 128, 128)  # Размеры 3D массива
syntwave_noise = generate_syntwave_noise(shape)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(syntwave_noise, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "syntwave.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]:.4f} {vert[1]:.4f} {vert[2]:.4f}\n")
    for face in faces:
        f.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")
print(f"Model saved as {filename}")

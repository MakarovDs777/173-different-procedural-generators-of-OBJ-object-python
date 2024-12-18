import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy.interpolate import interp1d
import os

# Генерация поверхности кожи
def generate_skin_surface(xmin, xmax, ymin, ymax, zmin, zmax, nx, ny):
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    X, Y = np.meshgrid(x, y)
    Z = np.ones(X.shape) * zmin
    return X, Y, Z

def generate_hair(X, Y, Z, num_hairs, hair_length, hair_radius):
    hair_x_tube = []
    hair_y_tube = []
    hair_z_tube = []

    for _ in range(num_hairs):
        hair_x = np.random.uniform(X.min(), X.max())
        hair_y = np.random.uniform(Y.min(), Y.max())
        hair_z = Z.min()

        hair_t = np.linspace(0, 1, 100)
        hair_x_interp = np.linspace(hair_x, hair_x, 100)
        hair_y_interp = np.linspace(hair_y, hair_y, 100)
        hair_z_interp = np.linspace(hair_z, hair_z + hair_length, 100)

        hair_theta = np.linspace(0, 2*np.pi, 100)

        hair_x_tube_local = []
        hair_y_tube_local = []
        hair_z_tube_local = []

        for i in range(len(hair_x_interp)):
            for j in range(len(hair_theta)):
                hair_x_tube_local.append(hair_x_interp[i] + hair_radius * np.cos(hair_theta[j]))
                hair_y_tube_local.append(hair_y_interp[i] + hair_radius * np.sin(hair_theta[j]))
                hair_z_tube_local.append(hair_z_interp[i])

        hair_x_tube.extend(hair_x_tube_local)
        hair_y_tube.extend(hair_y_tube_local)
        hair_z_tube.extend(hair_z_tube_local)

        # Добавить пустые значения для разделения труб
        hair_x_tube.extend([np.nan]*len(hair_theta))
        hair_y_tube.extend([np.nan]*len(hair_theta))
        hair_z_tube.extend([np.nan]*len(hair_theta))

    return hair_x_tube, hair_y_tube, hair_z_tube

# Визуализация поверхности и волос
def visualize_surface_and_hair(X, Y, Z, hair_x, hair_y, hair_z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.5)

    num_hairs = len(hair_x) // 100
    for i in range(num_hairs):
        hair_x_local = hair_x[i*100:(i+1)*100]
        hair_y_local = hair_y[i*100:(i+1)*100]
        hair_z_local = hair_z[i*100:(i+1)*100]
        ax.plot(hair_x_local, hair_y_local, hair_z_local, 'k-')

    plt.show()

# Сохранение файла
def save_file(X, Y, Z, hair_x, hair_y, hair_z):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "skin_and_hair.obj")
    with open(filename, "w") as f:
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                f.write(f"v {X[i, j]} {Z[i, j]} {Y[i, j]}\n")
        for i in range(len(hair_x)):
            f.write(f"v {hair_x[i]} {hair_z[i]} {hair_y[i]}\n")
        for i in range(X.shape[0] - 1):
            for j in range(X.shape[1] - 1):
                f.write(f"f {i * X.shape[1] + j + 1} {(i + 1) * X.shape[1] + j + 1} {(i + 1) * X.shape[1] + j + 2}\n")
                f.write(f"f {i * X.shape[1] + j + 1} {(i + 1) * X.shape[1] + j + 2} {i * X.shape[1] + j + 2}\n")
        num_hairs = len(hair_x) // 100
        for i in range(num_hairs):
            for j in range(100):
                idx1 = i * 100 + j
                idx2 = i * 100 + (j + 1) % 100
                idx3 = (i + 1) * 100 + (j + 1) % 100
                idx4 = (i + 1) * 100 + j

                f.write(f"f {X.shape[0] * X.shape[1] + idx1 + 1} {X.shape[0] * X.shape[1] + idx2 + 1} {X.shape[0] * X.shape[1] + idx3 + 1}\n")
                f.write(f"f {X.shape[0] * X.shape[1] + idx1 + 1} {X.shape[0] * X.shape[1] + idx3 + 1} {X.shape[0] * X.shape[1] + idx4 + 1}\n")
    print(f"Файл сохранен как {filename}")

# Основная функция
def main():
    X, Y, Z = generate_skin_surface(-10, 10, -10, 10, 0, 10, 100, 100)
    num_hairs = random.randint(3, 120)
    hair_length = 5
    hair_radius = 0.1
    hair_x, hair_y, hair_z = generate_hair(X, Y, Z, num_hairs, hair_length, hair_radius)
    visualize_surface_and_hair(X, Y, Z, hair_x, hair_y, hair_z)
    save_file(X, Y, Z, hair_x, hair_y, hair_z)

if __name__ == "__main__":
    main()

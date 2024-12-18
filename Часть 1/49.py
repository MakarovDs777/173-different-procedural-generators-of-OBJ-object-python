import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Генерация поверхности
def generate_surface(xmin, xmax, ymin, ymax, zmin, zmax, nx, ny):
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    return X, Y, Z

# Визуализация поверхности и волос
def visualize_surface_and_hair(X, Y, Z, hair_x, hair_y, hair_z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.5)
    ax.plot(hair_x, hair_y, hair_z, 'b-')
    plt.show()

# Генерация волос
def generate_hair(X, Y, Z, num_hairs, length, radius):
    hair_x = []
    hair_y = []
    hair_z = []
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if np.random.rand() < 0.1:  # вероятность появления волоса
                theta = np.linspace(0, 2 * np.pi, 10)
                for k in range(length):
                    for t in theta:
                        hair_x.append(X[i, j] + radius * np.cos(t))
                        hair_y.append(Y[i, j] + radius * np.sin(t))
                        hair_z.append(Z[i, j] + k * 0.1)
    return hair_x, hair_y, hair_z

# Сохранение файла
def save_file(X, Y, Z, hair_x, hair_y, hair_z):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "surface_and_hair.obj")
    with open(filename, "w") as f:
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                f.write(f"v {X[i, j]} {Y[i, j]} {Z[i, j]}\n")
        for i in range(len(hair_x)):
            f.write(f"v {hair_x[i]} {hair_y[i]} {hair_z[i]}\n")
        for i in range(X.shape[0] - 1):
            for j in range(X.shape[1] - 1):
                f.write(f"f {i * X.shape[1] + j + 1} {(i + 1) * X.shape[1] + j + 1} {(i + 1) * X.shape[1] + j + 2}\n")
                f.write(f"f {i * X.shape[1] + j + 1} {(i + 1) * X.shape[1] + j + 2} {i * X.shape[1] + j + 2}\n")
        num_hairs = len(hair_x) // 10 // 10
        for i in range(num_hairs):
            for j in range(10):
                for k in range(10):
                    idx1 = i * 10 * 10 + j * 10 + k
                    idx2 = i * 10 * 10 + j * 10 + (k + 1) % 10
                    idx3 = (i * 10 * 10 + (j + 1) * 10 + (k + 1) % 10)
                    idx4 = (i * 10 * 10 + (j + 1) * 10 + k)
                    f.write(f"f {X.shape[0] * X.shape[1] + idx1 + 1} {X.shape[0] * X.shape[1] + idx2 + 1} {X.shape[0] * X.shape[1] + idx3 + 1}\n")
                    f.write(f"f {X.shape[0] * X.shape[1] + idx1 + 1} {X.shape[0] * X.shape[1] + idx3 + 1} {X.shape[0] * X.shape[1] + idx4 + 1}\n")
    print(f"Файл сохранен как {filename}")

# Основная функция
def main():
    X, Y, Z = generate_surface(-10, 10, -10, 10, -10, 10, 100, 100)
    hair_x, hair_y, hair_z = generate_hair(X, Y, Z, 100, 10, 0.1)
    save_file(X, Y, Z, hair_x, hair_y, hair_z)

if __name__ == "__main__":
    main()

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import noise
import os

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
glTranslatef(0.0, 0.0, -30)
glRotatef(45, 1, 0, 0)  # Повернуть камеру на 45 градусов вокруг оси X

def generate_noise_2d(shape, x_offset, z_offset, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
    noise_map = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            noise_map[i][j] = noise.pnoise2((i + x_offset) / scale, (j + z_offset) / scale, octaves=octaves,
                                              persistence=persistence, lacunarity=lacunarity, repeatx=1024,
                                              repeaty=1024, base=42)
    return noise_map

def create_terrain(width, height, x_offset, z_offset):
    noise_map = generate_noise_2d((width, height), x_offset, z_offset)
    vertices = []
    for i in range(width):
        for j in range(height):
            x = i - width // 2
            z = j - height // 2
            y = noise_map[i][j] * 10
            vertices.append((x, y, z))
    return vertices

def create_tube(vertices, radius, slices):
    tube_vertices = []
    tube_faces = []

    for i in range(len(vertices) - 1):
        v1 = np.array(vertices[i])
        v2 = np.array(vertices[i + 1])

        direction = v2 - v1
        length = np.linalg.norm(direction)
        direction /= length  # Нормализация

        if np.linalg.norm(direction) == 0:
            continue
        perpendicular = np.cross(direction, np.array([0, 1, 0]))
        if np.linalg.norm(perpendicular) == 0:
            perpendicular = np.cross(direction, np.array([1, 0, 0]))
        
        perpendicular /= np.linalg.norm(perpendicular)  # Нормализация

        # Создание вершин и граней трубы
        for j in range(slices + 1):
            angle = 2 * np.pi * j / slices
            offset = radius * (np.cos(angle) * perpendicular + np.sin(angle) * np.cross(direction, perpendicular))
            current_vertex = v1 + offset
            
            tube_vertices.append(current_vertex)

            # Формирование граней
            if i < len(vertices) - 2:  # Проверка, чтобы не выйти за границы
                next_index = (i + 1) * (slices + 1) + j
                current_index = i * (slices + 1) + j
                next_j = (j + 1) % (slices + 1)

                # Создание двух треугольников
                tube_faces.append([current_index, next_index, next_index + 1])
                tube_faces.append([current_index, next_index + 1, current_index + 1])

    return tube_vertices, tube_faces

def save_to_obj(vertices, faces, filename):
    with open(filename, "w") as f:
        for vert in vertices:
            f.write(f"v {vert[0]:.4f} {vert[1]:.4f} {vert[2]:.4f}\n")
        for face in faces:
            f.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")
    print(f"Model saved as {filename}")
    # Функция для отрисовки трубы

def draw_tube(vertices, width, height, radius, slices):
    # Отрисовка труб сверху вниз
    for i in range(width):
        for j in range(height - 1):
            v1 = np.array(vertices[i * height + j])
            v2 = np.array(vertices[i * height + j + 1])

            direction = v2 - v1
            length = np.linalg.norm(direction)
            direction /= length  # Нормализация

            perpendicular = np.cross(direction, np.array([1, 0, 0]))
            if np.linalg.norm(perpendicular) == 0:
                continue
            perpendicular /= np.linalg.norm(perpendicular)  # Нормализация

            # Отрисовка трубы между v1 и v2
            glBegin(GL_QUAD_STRIP)
            for k in range(slices + 1):
                angle = 2 * np.pi * k / slices
                offset = radius * (np.cos(angle) * perpendicular + np.sin(angle) * np.cross(direction, perpendicular))

                glVertex3fv(v1 + offset)  # Вершина 1
                glVertex3fv(v2 + offset)  # Вершина 2
            glEnd()

    # Отрисовка труб справа налево
    for j in range(height):
        for i in range(width - 1, 0, -1):
            v1 = np.array(vertices[j * height + i])
            v2 = np.array(vertices[j * height + i - 1])

            direction = v2 - v1
            length = np.linalg.norm(direction)
            direction /= length  # Нормализация

            perpendicular = np.cross(direction, np.array([0, 1, 0]))
            if np.linalg.norm(perpendicular) == 0:
                continue
            perpendicular /= np.linalg.norm(perpendicular)  # Нормализация

            glBegin(GL_QUAD_STRIP)
            for k in range(slices + 1):
                angle = 2 * np.pi * k / slices
                offset = radius * (np.cos(angle) * perpendicular + np.sin(angle) * np.cross(direction, perpendicular))

                glVertex3fv(v1 + offset)  # Вершина 1
                glVertex3fv(v2 + offset)  # Вершина 2
            glEnd()

width, height = 20, 20
x_offset = 0
z_offset = 0
clock = pygame.time.Clock()
tube_radius = 0.25
slices = 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                z_offset += 5
            if event.key == pygame.K_s:
                z_offset -= 5
            if event.key == pygame.K_a:
                x_offset -= 5
            if event.key == pygame.K_d:
                x_offset += 5
            if event.key == pygame.K_r:  # Сохранение на нажатие R
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                terrain = create_terrain(width, height, x_offset, z_offset)
                tube_vertices, tube_faces = create_tube(terrain, tube_radius, slices)
                filename = os.path.join(desktop_path, "terrain_tube.obj")
                save_to_obj(tube_vertices, tube_faces, filename)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    vertices = create_terrain(width, height, x_offset, z_offset)
    tube_vertices, _ = create_tube(vertices, tube_radius, slices)  # Создаем данные труб
    draw_tube(vertices, width, height, radius=tube_radius, slices=slices)  # Рисуем трубы
    pygame.display.flip()
    clock.tick(60)

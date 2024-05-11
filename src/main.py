import os
import time
import math

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def rotate_point(cx, cy, angle, px, py):
    """Rotate a point around a given center in 2D."""
    s = math.sin(angle)
    c = math.cos(angle)
    px -= cx
    py -= cy
    xnew = px * c - py * s
    ynew = px * s + py * c
    return int(xnew + cx), int(ynew + cy)

def project_point_3d_to_2d(px, py, pz):
    """Project 3D point to 2D using simple perspective projection"""
    # Perspective projection factors
    focal_length = 200
    if pz:
        px = px * focal_length / pz
        py = py * focal_length / pz
    return int(px + 200), int(py + 100)

def draw_shape(canvas, vertices, edges):
    """Draw a shape defined by vertices and edges on the canvas."""
    for edge in edges:
        x0, y0 = vertices[edge[0]]
        x1, y1 = vertices[edge[1]]
        draw_line(canvas, x0, y0, x1, y1)

def draw_line(canvas, x0, y0, x1, y1):
    """Draw a line on the canvas using Bresenham's line algorithm."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        if 0 <= x0 < 400 and 0 <= y0 < 200:
            canvas[y0][x0] = '*'
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

def main():
    shape = input("Choose a shape (triangle/cube): ")
    angle = 0
    if shape == "triangle":
        vertices = [(100, 150), (200, 50), (300, 150)]
        edges = [(0, 1), (1, 2), (2, 0)]
    elif shape == "cube":
        # Define vertices of a cube centered at the origin (0,0,0)
        size = 50
        vertices = [
            (-size, -size, -size), (size, -size, -size),
            (size, size, -size), (-size, size, -size),
            (-size, -size, size), (size, -size, size),
            (size, size, size), (-size, size, size)
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

    while True:
        # Rotate vertices and project them if it's a cube
        if shape == "cube":
            rotated_vertices = [(
                math.cos(angle) * vx - math.sin(angle) * vz,
                vy,
                math.sin(angle) * vx + math.cos(angle) * vz
            ) for vx, vy, vz in vertices]
            projected_vertices = [project_point_3d_to_2d(vx, vy, vz) for vx, vy, vz in rotated_vertices]
        else:
            center_x, center_y = 200, 100
            projected_vertices = [rotate_point(center_x, center_y, math.radians(angle), vx, vy) for vx, vy in vertices]

        clear_screen()
        canvas = [[' ' for _ in range(400)] for _ in range(200)]
        draw_shape(canvas, projected_vertices, edges)
        for row in canvas:
            print(''.join(row))
        time.sleep(0.1)
        angle += 0.05

if __name__ == "__main__":
    main()

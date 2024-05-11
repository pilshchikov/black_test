import os
import time
import math

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def rotate_point(cx, cy, angle, px, py):
    """Rotate a point around a given center."""
    s = math.sin(angle)
    c = math.cos(angle)

    # translate point back to origin:
    px -= cx
    py -= cy

    # rotate point
    xnew = px * c - py * s
    ynew = px * s + py * c

    # translate point back:
    px = xnew + cx
    py = ynew + cy
    return int(px), int(py)

def draw_triangle(vertices):
    """Draw a triangle in the terminal using ASCII characters."""
    # Create a blank canvas
    canvas = [[' ' for _ in range(40)] for _ in range(20)]

    # Draw lines between vertices
    for i in range(3):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % 3]
        draw_line(canvas, x0, y0, x1, y1)

    # Print the canvas
    for row in canvas:
        print(''.join(row))

def draw_line(canvas, x0, y0, x1, y1):
    """Draw a line on the canvas using Bresenham's line algorithm."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        if 0 <= x0 < 40 and 0 <= y0 < 20:
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
    os.environ['TERM'] = 'xterm'  # Set TERM environment variable
    angle = 0
    vertices = [(10, 10), (20, 5), (30, 10)]  # Initial vertices of the triangle
    center_x, center_y = 20, 10  # Center for rotation

    while True:
        # Rotate all vertices
        rotated_vertices = [rotate_point(center_x, center_y, math.radians(angle), vx, vy) for vx, vy in vertices]
        clear_screen()
        draw_triangle(rotated_vertices)
        time.sleep(0.1)  # Control the speed of the animation
        angle += 2  # Increase the angle for rotation

if __name__ == "__main__":
    main()

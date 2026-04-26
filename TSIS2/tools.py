import pygame
import math


def draw_line(surface, start, end, color, size):
    pygame.draw.line(surface, color, start, end, size)


def get_rectangle_data(start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    return x, y, w, h


def draw_rect(surface, start, end, color, size):
    x, y, w, h = get_rectangle_data(start, end)
    pygame.draw.rect(surface, color, (x, y, w, h), size)


def draw_circle(surface, center, radius, color, size):
    if radius > 0:
        pygame.draw.circle(surface, color, center, radius, size)


def draw_square(surface, color, start, end, width=2):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = min(abs(dx), abs(dy))

    x = start[0]
    y = start[1]

    if dx < 0:
        x -= side
    if dy < 0:
        y -= side

    pygame.draw.rect(surface, color, (x, y, side, side), width)


def draw_right_triangle(surface, color, start, end, width=2):
    points = [
        start,
        (start[0], end[1]),
        end
    ]
    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start, end, width=2):
    side = abs(end[0] - start[0])

    if side == 0:
        return

    if end[0] >= start[0]:
        x1 = start[0]
        x2 = start[0] + side
    else:
        x1 = start[0]
        x2 = start[0] - side

    y_base = end[1]
    height = int((math.sqrt(3) / 2) * side)

    top_x = (x1 + x2) // 2
    top_y = y_base - height

    points = [
        (x1, y_base),
        (x2, y_base),
        (top_x, top_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, start, end, width=2):
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2

    points = [
        (center_x, start[1]),
        (end[0], center_y),
        (center_x, end[1]),
        (start[0], center_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_text(surface, text, pos, color, font):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)


def to_pygame_color(color):
    if isinstance(color, pygame.Color):
        return color

    if len(color) == 3:
        return pygame.Color(color[0], color[1], color[2], 255)

    return pygame.Color(color[0], color[1], color[2], color[3])


def flood_fill(surface, x, y, new_color):
    width = surface.get_width()
    height = surface.get_height()

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))
    new_color = to_pygame_color(new_color)

    if target_color == new_color:
        return

    stack = [(x, y)]

    surface.lock()

    try:
        while stack:
            px, py = stack.pop()

            if surface.get_at((px, py)) != target_color:
                continue

            surface.set_at((px, py), new_color)

            if px > 0:
                stack.append((px - 1, py))
            if px < width - 1:
                stack.append((px + 1, py))
            if py > 0:
                stack.append((px, py - 1))
            if py < height - 1:
                stack.append((px, py + 1))

    finally:
        surface.unlock()
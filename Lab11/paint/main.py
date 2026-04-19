import pygame
import sys
import math

pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 600
TOOLBAR_HEIGHT = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (220, 220, 220)

# Canvas settings
BG_COLOR = WHITE
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(BG_COLOR)

# Initial tool settings
current_color = BLACK
tool = "brush"
drawing = False
start_pos = None
brush_size = 5
eraser_size = 18

# Font
font = pygame.font.SysFont("Arial", 18)

def draw_ui():
    """Draw the top toolbar with tools, colors, and current mode."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    tool_text_1 = font.render("B-Brush  R-Rectangle  C-Circle  E-Eraser  S-Square", True, BLACK)
    tool_text_2 = font.render("T-RightTriangle  Q-EquilateralTriangle  H-Rhombus", True, BLACK)
    color_text = font.render("1-Black  2-Red  3-Green  4-Blue  5-Yellow", True, BLACK)

    screen.blit(tool_text_1, (10, 5))
    screen.blit(tool_text_2, (10, 23))
    screen.blit(color_text, (10, 41))

    mode_text = font.render(f"Tool: {tool}", True, BLACK)
    screen.blit(mode_text, (700, 20))

def to_canvas_pos(pos):
    """Convert screen coordinates to canvas coordinates."""
    return (pos[0], pos[1] - TOOLBAR_HEIGHT)

def get_rectangle_data(start, end):
    """Return x, y, width, height for a rectangle."""
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    return x, y, w, h

def draw_square(surface, color, start, end, width=2):
    """Draw a square using the smaller side length."""
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
    """Draw a right triangle using drag area."""
    points = [
        start,
        (start[0], end[1]),
        end
    ]
    pygame.draw.polygon(surface, color, points, width)

def draw_equilateral_triangle(surface, color, start, end, width=2):
    """Draw an equilateral triangle based on horizontal side."""
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

    points = [(x1, y_base), (x2, y_base), (top_x, top_y)]
    pygame.draw.polygon(surface, color, points, width)

def draw_rhombus(surface, color, start, end, width=2):
    """Draw a rhombus inside the dragged area."""
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2

    points = [
        (center_x, start[1]),   # top
        (end[0], center_y),     # right
        (center_x, end[1]),     # bottom
        (start[0], center_y)    # left
    ]
    pygame.draw.polygon(surface, color, points, width)

running = True
while running:
    preview = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle keyboard tool/color selection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rectangle"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_s:
                tool = "square"
            elif event.key == pygame.K_t:
                tool = "right_triangle"
            elif event.key == pygame.K_q:
                tool = "equilateral_triangle"
            elif event.key == pygame.K_h:
                tool = "rhombus"
            elif event.key == pygame.K_1:
                current_color = BLACK
            elif event.key == pygame.K_2:
                current_color = RED
            elif event.key == pygame.K_3:
                current_color = GREEN
            elif event.key == pygame.K_4:
                current_color = BLUE
            elif event.key == pygame.K_5:
                current_color = YELLOW

        # Start drawing
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] > TOOLBAR_HEIGHT:
                drawing = True
                start_pos = to_canvas_pos(event.pos)

                if tool == "brush":
                    pygame.draw.circle(canvas, current_color, start_pos, brush_size)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, BG_COLOR, start_pos, eraser_size)

        # Continue drawing with brush or eraser
        if event.type == pygame.MOUSEMOTION and drawing:
            if event.pos[1] > TOOLBAR_HEIGHT:
                current_pos = to_canvas_pos(event.pos)

                if tool == "brush":
                    pygame.draw.circle(canvas, current_color, current_pos, brush_size)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, BG_COLOR, current_pos, eraser_size)

        # Finalize shape on mouse release
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos and event.pos[1] > TOOLBAR_HEIGHT:
                end_pos = to_canvas_pos(event.pos)

                if tool == "rectangle":
                    x, y, w, h = get_rectangle_data(start_pos, end_pos)
                    pygame.draw.rect(canvas, current_color, (x, y, w, h), 2)

                elif tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

                elif tool == "square":
                    draw_square(canvas, current_color, start_pos, end_pos, 2)

                elif tool == "right_triangle":
                    draw_right_triangle(canvas, current_color, start_pos, end_pos, 2)

                elif tool == "equilateral_triangle":
                    draw_equilateral_triangle(canvas, current_color, start_pos, end_pos, 2)

                elif tool == "rhombus":
                    draw_rhombus(canvas, current_color, start_pos, end_pos, 2)

            drawing = False
            start_pos = None

    # Draw preview while dragging shapes
    if drawing and start_pos:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] > TOOLBAR_HEIGHT:
            current_pos = to_canvas_pos(mouse_pos)

            if tool == "rectangle":
                x, y, w, h = get_rectangle_data(start_pos, current_pos)
                pygame.draw.rect(preview, current_color, (x, y, w, h), 2)

            elif tool == "circle":
                radius = int(((current_pos[0] - start_pos[0]) ** 2 + (current_pos[1] - start_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(preview, current_color, start_pos, radius, 2)

            elif tool == "square":
                draw_square(preview, current_color, start_pos, current_pos, 2)

            elif tool == "right_triangle":
                draw_right_triangle(preview, current_color, start_pos, current_pos, 2)

            elif tool == "equilateral_triangle":
                draw_equilateral_triangle(preview, current_color, start_pos, current_pos, 2)

            elif tool == "rhombus":
                draw_rhombus(preview, current_color, start_pos, current_pos, 2)

    screen.fill(WHITE)
    draw_ui()
    screen.blit(preview, (0, TOOLBAR_HEIGHT))

    pygame.display.update()
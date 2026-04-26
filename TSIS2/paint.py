import pygame
import sys
import datetime

from tools import (
    flood_fill,
    draw_line,
    draw_rect,
    draw_circle,
    draw_square,
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_rhombus,
    draw_text
)

pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 600
TOOLBAR_HEIGHT = 100
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (160, 160, 160)

# Canvas
canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

# State
current_color = BLACK
tool = "pencil"
drawing = False
start_pos = None
last_pos = None

brush_size = 5

text_active = False
text_buffer = ""
text_pos = None

font = pygame.font.SysFont("Arial", 16)
small_font = pygame.font.SysFont("Arial", 14)

clock = pygame.time.Clock()

# Tool buttons
tool_buttons = {
    "pencil": pygame.Rect(10, 5, 70, 24),
    "line": pygame.Rect(85, 5, 70, 24),
    "fill": pygame.Rect(160, 5, 70, 24),
    "text": pygame.Rect(235, 5, 70, 24),
    "rectangle": pygame.Rect(310, 5, 70, 24),
    "circle": pygame.Rect(385, 5, 70, 24),
    "eraser": pygame.Rect(460, 5, 70, 24),
    "square": pygame.Rect(535, 5, 70, 24),
    "right_triangle": pygame.Rect(610, 5, 70, 24),
    "equilateral_triangle": pygame.Rect(685, 5, 80, 24),
    "rhombus": pygame.Rect(770, 5, 80, 24),
}

tool_labels = {
    "pencil": "Pencil",
    "line": "Line",
    "fill": "Fill",
    "text": "Text",
    "rectangle": "Rect",
    "circle": "Circle",
    "eraser": "Eraser",
    "square": "Square",
    "right_triangle": "R-Tri",
    "equilateral_triangle": "Eq-Tri",
    "rhombus": "Rhombus",
}

# Color buttons
colors = [BLACK, RED, GREEN, BLUE, YELLOW, ORANGE]
color_buttons = {}

for i, color in enumerate(colors):
    color_buttons[color] = pygame.Rect(10 + i * 36, 38, 28, 24)

# Brush size buttons
size_buttons = {
    2: pygame.Rect(260, 38, 45, 24),
    5: pygame.Rect(310, 38, 45, 24),
    10: pygame.Rect(360, 38, 45, 24),
}


def to_canvas_pos(pos):
    """Convert screen coordinates to canvas coordinates."""
    return pos[0], pos[1] - TOOLBAR_HEIGHT


def is_inside_canvas(pos):
    return pos[1] >= TOOLBAR_HEIGHT


def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # Tool buttons
    for tool_name, rect in tool_buttons.items():
        button_color = DARK_GRAY if tool == tool_name else (200, 200, 200)
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

        label = small_font.render(tool_labels[tool_name], True, BLACK)
        screen.blit(label, (rect.x + 5, rect.y + 4))

    # Color buttons
    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

        if current_color == color:
            pygame.draw.rect(screen, BLUE, rect, 3)

    color_hint = small_font.render("Colors: 1-Black  2-Red  3-Green  4-Blue  5-Yellow  6-Orange", True, BLACK)
    screen.blit(color_hint, (10, 66))

    # Brush size buttons
    size_title = small_font.render("Size:", True, BLACK)
    screen.blit(size_title, (220, 42))

    for size, rect in size_buttons.items():
        button_color = DARK_GRAY if brush_size == size else (200, 200, 200)
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

        label = small_font.render(str(size), True, BLACK)
        screen.blit(label, (rect.x + 15, rect.y + 4))

    status = small_font.render(
        f"Tool: {tool} | Brush size: {brush_size} | F1=2 F2=5 F3=10 | Ctrl+S Save",
        True,
        BLACK
    )
    screen.blit(status, (420, 42))

    keys = small_font.render(
        "Keys: P Pencil, L Line, F Fill, X Text, R Rect, C Circle, E Eraser, S Square, A RightTri, Q EqTri, H Rhombus",
        True,
        BLACK
    )
    screen.blit(keys, (10, 83))


running = True

while running:
    preview = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            # Save canvas
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = f"canvas_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                pygame.image.save(canvas, filename)
                print("Saved:", filename)

            # Text input mode
            elif text_active:
                if event.key == pygame.K_RETURN:
                    draw_text(canvas, text_buffer, text_pos, current_color, font)
                    text_active = False
                    text_buffer = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_buffer = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]

                elif event.unicode:
                    text_buffer += event.unicode

            # Normal shortcuts
            else:
                if event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_x:
                    tool = "text"
                elif event.key == pygame.K_r:
                    tool = "rectangle"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_a:
                    tool = "right_triangle"
                elif event.key == pygame.K_q:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"

                # Colors
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
                elif event.key == pygame.K_6:
                    current_color = ORANGE

                # Brush sizes
                elif event.key == pygame.K_F1:
                    brush_size = 2
                elif event.key == pygame.K_F2:
                    brush_size = 5
                elif event.key == pygame.K_F3:
                    brush_size = 10

        # Mouse down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                continue

            # Click on toolbar
            if event.pos[1] < TOOLBAR_HEIGHT:
                for name, rect in tool_buttons.items():
                    if rect.collidepoint(event.pos):
                        tool = name
                        text_active = False
                        text_buffer = ""
                        text_pos = None

                for color, rect in color_buttons.items():
                    if rect.collidepoint(event.pos):
                        current_color = color

                for size, rect in size_buttons.items():
                    if rect.collidepoint(event.pos):
                        brush_size = size

                continue

            # Click on canvas
            canvas_pos = to_canvas_pos(event.pos)

            if tool == "fill":
                flood_fill(canvas, canvas_pos[0], canvas_pos[1], current_color)

            elif tool == "text":
                text_active = True
                text_buffer = ""
                text_pos = canvas_pos

            else:
                drawing = True
                start_pos = canvas_pos
                last_pos = canvas_pos

                if tool == "pencil":
                    pygame.draw.circle(canvas, current_color, canvas_pos, brush_size // 2)

                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, canvas_pos, brush_size // 2)

        # Mouse motion
        if event.type == pygame.MOUSEMOTION:
            if drawing and is_inside_canvas(event.pos):
                current_pos = to_canvas_pos(event.pos)

                if tool == "pencil":
                    draw_line(canvas, last_pos, current_pos, current_color, brush_size)
                    last_pos = current_pos

                elif tool == "eraser":
                    draw_line(canvas, last_pos, current_pos, WHITE, brush_size)
                    last_pos = current_pos

        # Mouse up
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos and is_inside_canvas(event.pos):
                end_pos = to_canvas_pos(event.pos)

                if tool == "line":
                    draw_line(canvas, start_pos, end_pos, current_color, brush_size)

                elif tool == "rectangle":
                    draw_rect(canvas, start_pos, end_pos, current_color, brush_size)

                elif tool == "circle":
                    radius = int(
                        ((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5
                    )
                    draw_circle(canvas, start_pos, radius, current_color, brush_size)

                elif tool == "square":
                    draw_square(canvas, current_color, start_pos, end_pos, brush_size)

                elif tool == "right_triangle":
                    draw_right_triangle(canvas, current_color, start_pos, end_pos, brush_size)

                elif tool == "equilateral_triangle":
                    draw_equilateral_triangle(canvas, current_color, start_pos, end_pos, brush_size)

                elif tool == "rhombus":
                    draw_rhombus(canvas, current_color, start_pos, end_pos, brush_size)

            drawing = False
            start_pos = None
            last_pos = None

    # Live preview for shapes and line
    if drawing and start_pos:
        mouse_pos = pygame.mouse.get_pos()

        if is_inside_canvas(mouse_pos):
            current_pos = to_canvas_pos(mouse_pos)

            if tool == "line":
                draw_line(preview, start_pos, current_pos, current_color, brush_size)

            elif tool == "rectangle":
                draw_rect(preview, start_pos, current_pos, current_color, brush_size)

            elif tool == "circle":
                radius = int(
                    ((current_pos[0] - start_pos[0]) ** 2 + (current_pos[1] - start_pos[1]) ** 2) ** 0.5
                )
                draw_circle(preview, start_pos, radius, current_color, brush_size)

            elif tool == "square":
                draw_square(preview, current_color, start_pos, current_pos, brush_size)

            elif tool == "right_triangle":
                draw_right_triangle(preview, current_color, start_pos, current_pos, brush_size)

            elif tool == "equilateral_triangle":
                draw_equilateral_triangle(preview, current_color, start_pos, current_pos, brush_size)

            elif tool == "rhombus":
                draw_rhombus(preview, current_color, start_pos, current_pos, brush_size)

    # Text preview
    if text_active and text_pos is not None:
        draw_text(preview, text_buffer, text_pos, current_color, font)

    # Render
    screen.fill(WHITE)
    draw_ui()
    screen.blit(preview, (0, TOOLBAR_HEIGHT))

    pygame.display.update()
    clock.tick(60)
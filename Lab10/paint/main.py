import pygame
import sys

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
font = pygame.font.SysFont("Arial", 20)

def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    tool_text = font.render("B-Brush  R-Rectangle  C-Circle  E-Eraser", True, BLACK)
    color_text = font.render("1-Black  2-Red  3-Green  4-Blue  5-Yellow", True, BLACK)

    screen.blit(tool_text, (10, 8))
    screen.blit(color_text, (10, 32))

    mode_text = font.render(f"Tool: {tool} | Color: {current_color}", True, BLACK)
    screen.blit(mode_text, (520, 20))

def to_canvas_pos(pos):
    return (pos[0], pos[1] - TOOLBAR_HEIGHT)

running = True
while running:
    preview = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rectangle"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] > TOOLBAR_HEIGHT:
                drawing = True
                start_pos = to_canvas_pos(event.pos)

                if tool == "brush":
                    pygame.draw.circle(canvas, current_color, start_pos, brush_size)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, BG_COLOR, start_pos, eraser_size)

        if event.type == pygame.MOUSEMOTION and drawing:
            if event.pos[1] > TOOLBAR_HEIGHT:
                current_pos = to_canvas_pos(event.pos)

                if tool == "brush":
                    pygame.draw.circle(canvas, current_color, current_pos, brush_size)

                elif tool == "eraser":
                    pygame.draw.circle(canvas, BG_COLOR, current_pos, eraser_size)

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos and event.pos[1] > TOOLBAR_HEIGHT:
                end_pos = to_canvas_pos(event.pos)

                if tool == "rectangle":
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(start_pos[0] - end_pos[0])
                    h = abs(start_pos[1] - end_pos[1])
                    pygame.draw.rect(canvas, current_color, (x, y, w, h), 2)

                elif tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

            drawing = False
            start_pos = None

    if drawing and start_pos:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] > TOOLBAR_HEIGHT:
            current_pos = to_canvas_pos(mouse_pos)

            if tool == "rectangle":
                x = min(start_pos[0], current_pos[0])
                y = min(start_pos[1], current_pos[1])
                w = abs(start_pos[0] - current_pos[0])
                h = abs(start_pos[1] - current_pos[1])
                pygame.draw.rect(preview, current_color, (x, y, w, h), 2)

            elif tool == "circle":
                radius = int(((current_pos[0] - start_pos[0]) ** 2 + (current_pos[1] - start_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(preview, current_color, start_pos, radius, 2)

    screen.fill(WHITE)
    draw_ui()
    screen.blit(preview, (0, TOOLBAR_HEIGHT))

    pygame.display.update()
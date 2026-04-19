import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

x, y = WIDTH // 2, HEIGHT // 2
radius = 25
step = 20

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x - step >= radius:
        x -= step
    if keys[pygame.K_RIGHT] and x + step <= WIDTH - radius:
        x += step
    if keys[pygame.K_UP] and y - step >= radius:
        y -= step
    if keys[pygame.K_DOWN] and y + step <= HEIGHT - radius:
        y += step

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
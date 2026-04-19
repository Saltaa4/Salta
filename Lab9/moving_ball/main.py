import pygame
from ball import move_ball

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)

x, y = WIDTH // 2, HEIGHT // 2
radius = 25
step = 20

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # передаём только нужные кнопки
    key_states = [
        keys[pygame.K_LEFT],
        keys[pygame.K_RIGHT],
        keys[pygame.K_UP],
        keys[pygame.K_DOWN]
    ]

    x, y = move_ball(x, y, key_states, step, WIDTH, HEIGHT, radius)

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
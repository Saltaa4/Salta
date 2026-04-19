import pygame
from pathlib import Path
from clock import get_time, get_angles, draw_hand

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "images"

clock_img = pygame.image.load(str(IMG_DIR / "mickeyclock.jpeg"))
clock_img = pygame.transform.scale(clock_img, (WIDTH, HEIGHT))

hand = pygame.image.load(str(IMG_DIR / "right_hand.png")).convert_alpha()

CENTER = (300, 306)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    minutes, seconds = get_time(True)
    min_angle, sec_angle = get_angles(minutes, seconds)

    screen.blit(clock_img, (0, 0))

    draw_hand(screen, hand, CENTER, min_angle, 0.7)
    draw_hand(screen, hand, CENTER, sec_angle, 0.85)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
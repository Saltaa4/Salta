import math
from datetime import datetime
from pathlib import Path
import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "images"

clock_img = pygame.image.load(str(IMG_DIR / "mickeyclock.jpeg")).convert()
clock_img = pygame.transform.scale(clock_img, (WIDTH, HEIGHT))

hand_img = pygame.image.load(str(IMG_DIR / "right_hand.png")).convert_alpha()

CENTER = (300, 306)

def draw_rotated_hand(surface, hand_img, angle_deg, length_scale=1.0):
    w = int(hand_img.get_width() * length_scale)
    h = int(hand_img.get_height() * length_scale)
    scaled = pygame.transform.smoothscale(hand_img, (w, h))

    base = scaled.get_rect()
    base.midleft = CENTER

    rotated = pygame.transform.rotate(scaled, angle_deg)

    offset = pygame.math.Vector2(base.center) - pygame.math.Vector2(CENTER)
    rotated_offset = offset.rotate(-angle_deg)
    rotated_center = (CENTER[0] + rotated_offset.x, CENTER[1] + rotated_offset.y)

    rect = rotated.get_rect(center=rotated_center)
    surface.blit(rotated, rect)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.now()
    seconds = now.second
    minutes = now.minute + seconds / 60

    sec_angle = -((seconds * 6) - 90)
    min_angle = -((minutes * 6) - 90)

    screen.blit(clock_img, (0, 0))

    draw_rotated_hand(screen, hand_img, min_angle, 0.68)
    draw_rotated_hand(screen, hand_img, sec_angle, 0.82)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
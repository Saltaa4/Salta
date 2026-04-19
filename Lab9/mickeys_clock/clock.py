import pygame
from datetime import datetime

def get_time(use_real_time=True, test_minute=10, test_second=30):
    if use_real_time:
        now = datetime.now()
        seconds = now.second
        minutes = now.minute + seconds / 60
    else:
        seconds = test_second
        minutes = test_minute + seconds / 60

    return minutes, seconds


def get_angles(minutes, seconds):
    sec_angle = -((seconds * 6) - 90)
    min_angle = -((minutes * 6) - 90)
    return min_angle, sec_angle


def draw_hand(screen, hand_img, center, angle, scale):
    w = int(hand_img.get_width() * scale)
    h = int(hand_img.get_height() * scale)
    scaled = pygame.transform.smoothscale(hand_img, (w, h))

    base = scaled.get_rect()
    base.midleft = center

    rotated = pygame.transform.rotate(scaled, angle)

    offset = pygame.math.Vector2(base.center) - pygame.math.Vector2(center)
    rotated_offset = offset.rotate(-angle)
    rotated_center = (center[0] + rotated_offset.x, center[1] + rotated_offset.y)

    rect = rotated.get_rect(center=rotated_center)
    screen.blit(rotated, rect)
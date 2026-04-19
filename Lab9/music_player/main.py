import pygame
import os
from player import play, stop, next_track, prev_track, get_current_track

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont(None, 36)

running = True

while running:
    screen.fill((0, 0, 0))

    track_name = os.path.basename(get_current_track())
    text = font.render(f"Track: {track_name}", True, (255, 255, 255))
    screen.blit(text, (50, 140))

    hint = font.render("P-Play  S-Stop  N-Next  B-Back  Q-Quit", True, (255, 255, 255))
    screen.blit(hint, (50, 220))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play()
            elif event.key == pygame.K_s:
                stop()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                prev_track()
            elif event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()
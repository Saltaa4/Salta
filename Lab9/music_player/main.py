import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 36)

tracks = [
    "music/track1.wav",
    "music/track2.wav",
    "music/track3.wav"
]

current = 0

def play():
    pygame.mixer.music.load(tracks[current])
    pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()

def next_track():
    global current
    current = (current + 1) % len(tracks)
    play()

def prev_track():
    global current
    current = (current - 1) % len(tracks)
    play()

running = True

while running:
    screen.fill((0, 0, 0))

    text = font.render(f"Track: {os.path.basename(tracks[current])}", True, (255,255,255))
    screen.blit(text, (50, 150))

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
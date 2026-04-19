import pygame

current = 0
tracks = [
    "music/track1.wav",
    "music/track2.wav",
    "music/track3.wav"
]

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

def get_current_track():
    return tracks[current]
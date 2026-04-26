import sys
from pathlib import Path

import pygame

from persistence import (
    load_settings,
    save_settings,
    load_leaderboard,
    add_leaderboard_entry,
)
from racer import RacerGame, load_game_assets
from ui import UI


BASE_DIR = Path(__file__).resolve().parent
WIDTH, HEIGHT = 400, 600
FPS = 60


def load_sound(path):
    try:
        if path.exists():
            return pygame.mixer.Sound(str(path))
    except pygame.error:
        return None
    return None


def play_click(sound, settings):
    if settings.get("sound", True) and sound:
        sound.play()


def apply_music(settings, music_path):
    """Включает или выключает фоновую музыку в зависимости от настройки звука."""
    if settings.get("sound", True):
        if not pygame.mixer.music.get_busy() and music_path.exists():
            try:
                pygame.mixer.music.load(str(music_path))
                pygame.mixer.music.play(-1)
            except pygame.error:
                pass
    else:
        pygame.mixer.music.stop()


def username_screen(screen, clock, ui, settings, click_sound):
    username = settings.get("username", "Player")

    while True:
        ui.draw_username_screen(username)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    username = username.strip() or "Player"
                    settings["username"] = username
                    save_settings(settings)
                    play_click(click_sound, settings)
                    return username

                if event.key == pygame.K_ESCAPE:
                    return None

                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.unicode and len(username) < 12:
                    if event.unicode.isalnum() or event.unicode in "_- ":
                        username += event.unicode

        clock.tick(FPS)


def leaderboard_screen(screen, clock, ui, leaderboard):
    while True:
        ui.draw_leaderboard_screen(leaderboard)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_b):
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ui.back_button.collidepoint(event.pos):
                    return

        clock.tick(FPS)


def settings_screen(screen, clock, ui, settings, sounds, music_path):
    click_sound = sounds.get("click")

    while True:
        ui.draw_settings_screen(settings)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_b):
                    save_settings(settings)
                    return

                if event.key == pygame.K_1:
                    settings["sound"] = not settings.get("sound", True)
                    apply_music(settings, music_path)
                    play_click(click_sound, settings)

                elif event.key == pygame.K_2:
                    colors = ["blue", "red", "green", "yellow"]
                    current = settings.get("car_color", "blue")
                    index = colors.index(current) if current in colors else 0
                    settings["car_color"] = colors[(index + 1) % len(colors)]
                    play_click(click_sound, settings)

                elif event.key == pygame.K_3:
                    difficulties = ["easy", "normal", "hard"]
                    current = settings.get("difficulty", "normal")
                    index = difficulties.index(current) if current in difficulties else 1
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                    play_click(click_sound, settings)

                save_settings(settings)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ui.settings_sound_button.collidepoint(event.pos):
                    settings["sound"] = not settings.get("sound", True)
                    apply_music(settings, music_path)
                    play_click(click_sound, settings)

                elif ui.settings_color_button.collidepoint(event.pos):
                    colors = ["blue", "red", "green", "yellow"]
                    current = settings.get("car_color", "blue")
                    index = colors.index(current) if current in colors else 0
                    settings["car_color"] = colors[(index + 1) % len(colors)]
                    play_click(click_sound, settings)

                elif ui.settings_difficulty_button.collidepoint(event.pos):
                    difficulties = ["easy", "normal", "hard"]
                    current = settings.get("difficulty", "normal")
                    index = difficulties.index(current) if current in difficulties else 1
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                    play_click(click_sound, settings)

                elif ui.back_button.collidepoint(event.pos):
                    save_settings(settings)
                    return

                save_settings(settings)

        clock.tick(FPS)


def game_over_screen(screen, clock, ui, result, leaderboard, settings, click_sound):
    while True:
        ui.draw_game_over_screen(result)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    play_click(click_sound, settings)
                    return "retry"

                if event.key in (pygame.K_m, pygame.K_ESCAPE):
                    play_click(click_sound, settings)
                    return "menu"

                if event.key == pygame.K_l:
                    leaderboard_screen(screen, clock, ui, leaderboard)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ui.retry_button.collidepoint(event.pos):
                    play_click(click_sound, settings)
                    return "retry"

                if ui.menu_button.collidepoint(event.pos):
                    play_click(click_sound, settings)
                    return "menu"

        clock.tick(FPS)


def run_game(screen, clock, ui, assets, sounds, settings):
    game = RacerGame(screen, assets, sounds, settings)

    while True:
        result = game.run_frame()

        if result is not None:
            username = settings.get("username", "Player")
            entry = {
                "name": username,
                "score": result["score"],
                "distance": result["distance"],
                "coins": result["coins"],
            }
            leaderboard = add_leaderboard_entry(entry)
            return result, leaderboard

        clock.tick(FPS)


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer Game")
    clock = pygame.time.Clock()

    settings = load_settings()
    leaderboard = load_leaderboard()

    ui = UI(screen, WIDTH, HEIGHT)

    assets = load_game_assets(BASE_DIR, WIDTH, HEIGHT)

    sounds_dir = BASE_DIR / "assets" / "sounds"
    sounds = {
        "click": load_sound(sounds_dir / "button_click.mp3"),
        "collision": load_sound(sounds_dir / "collision.mp3"),
        "powerup": load_sound(sounds_dir / "sound_for_amplifiers.mp3"),
        "fail": load_sound(sounds_dir / "when_user_fail.mp3"),
    }

    music_path = sounds_dir / "background_music.mp3"
    apply_music(settings, music_path)

    while True:
        ui.draw_main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_click(sounds["click"], settings)
                    username = username_screen(screen, clock, ui, settings, sounds["click"])
                    if username is None:
                        continue

                    while True:
                        result, leaderboard = run_game(screen, clock, ui, assets, sounds, settings)
                        action = game_over_screen(
                            screen, clock, ui, result, leaderboard, settings, sounds["click"]
                        )
                        if action == "menu":
                            break

                elif event.key == pygame.K_2:
                    play_click(sounds["click"], settings)
                    leaderboard_screen(screen, clock, ui, leaderboard)

                elif event.key == pygame.K_3:
                    play_click(sounds["click"], settings)
                    settings_screen(screen, clock, ui, settings, sounds, music_path)

                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ui.play_button.collidepoint(event.pos):
                    play_click(sounds["click"], settings)
                    username = username_screen(screen, clock, ui, settings, sounds["click"])
                    if username is None:
                        continue

                    while True:
                        result, leaderboard = run_game(screen, clock, ui, assets, sounds, settings)
                        action = game_over_screen(
                            screen, clock, ui, result, leaderboard, settings, sounds["click"]
                        )
                        if action == "menu":
                            break

                elif ui.leaderboard_button.collidepoint(event.pos):
                    play_click(sounds["click"], settings)
                    leaderboard_screen(screen, clock, ui, leaderboard)

                elif ui.settings_button.collidepoint(event.pos):
                    play_click(sounds["click"], settings)
                    settings_screen(screen, clock, ui, settings, sounds, music_path)

                elif ui.quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
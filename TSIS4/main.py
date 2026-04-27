# main.py
import sys
import os
import json
import pygame

os.chdir(os.path.dirname(__file__))

from config import WIDTH, HEIGHT, WHITE, BLACK, GRAY, DARK_GRAY, GREEN, RED, YELLOW, BLUE, CYAN, ORANGE, PURPLE
from game import SnakeGame

# DB import with graceful fallback
try:
    import db as _db
    _db.init_db()
    DB_OK = True
except Exception as e:
    print(f"[DB] Not connected: {e}")
    DB_OK = False

# ── Settings (inline, no separate settings.py) ─────────────────────────────────
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")
SETTINGS_DEFAULTS = {"snake_color": [100, 220, 100], "grid": False, "sound": True}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in SETTINGS_DEFAULTS.items():
                data.setdefault(k, v)
            return data
        except Exception:
            pass
    return SETTINGS_DEFAULTS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


# ── Tiny UI helpers ────────────────────────────────────────────────────────────

def _font(size=22):
    return pygame.font.SysFont("Arial", size)


def draw_button(screen, rect, text, font,
                fill=(70, 70, 70), text_color=WHITE, hover=False):
    color = tuple(min(255, c + 30) for c in fill) if hover else fill
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    surf = font.render(text, True, text_color)
    r    = surf.get_rect(center=rect.center)
    screen.blit(surf, r)


def text_center(screen, text, y, font, color=WHITE):
    surf = font.render(text, True, color)
    screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))


def mouse_hover(rect):
    return rect.collidepoint(pygame.mouse.get_pos())


# ── Screens ───────────────────────────────────────────────────────────────────

def username_screen(screen, clock, current_name="Player"):
    font_big  = _font(36)
    font_mid  = _font(22)
    username  = current_name
    btn_ok    = pygame.Rect(WIDTH // 2 - 100, 320, 200, 44)

    while True:
        screen.fill((20, 20, 35))
        text_center(screen, "SNAKE GAME", 60, font_big, GREEN)
        text_center(screen, "Enter your username:", 140, font_mid)

        box = pygame.Rect(WIDTH // 2 - 140, 175, 280, 44)
        pygame.draw.rect(screen, (50, 50, 70), box, border_radius=6)
        pygame.draw.rect(screen, GREEN, box, 2, border_radius=6)
        surf = font_mid.render(username + "|", True, WHITE)
        screen.blit(surf, (box.x + 8, box.y + 10))

        draw_button(screen, btn_ok, "START", font_mid,
                    fill=(30, 140, 30), hover=mouse_hover(btn_ok))

        text_center(screen, "Press Enter to start  |  Esc = back", 390, _font(16), GRAY)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return username.strip() or "Player"
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.unicode and len(username) < 14:
                    if event.unicode.isalnum() or event.unicode in "_- ":
                        username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_ok.collidepoint(event.pos):
                    return username.strip() or "Player"

        clock.tick(60)


def leaderboard_screen(screen, clock):
    font_big  = _font(32)
    font_mid  = _font(18)
    font_sm   = _font(15)
    btn_back  = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 60, 200, 40)

    rows = []
    if DB_OK:
        try:
            rows = _db.get_leaderboard(10)
        except Exception:
            rows = []

    while True:
        screen.fill((15, 15, 30))
        text_center(screen, "TOP 10 LEADERBOARD", 18, font_big, YELLOW)

        if not rows:
            text_center(screen, "No records yet (DB not connected)", 180, font_mid, GRAY)
        else:
            headers = ["#", "Player", "Score", "Level", "Date"]
            col_x   = [20, 60, 220, 310, 380]
            y = 70
            for hx, ht in zip(col_x, headers):
                surf = font_sm.render(ht, True, CYAN)
                screen.blit(surf, (hx, y))
            y += 22
            pygame.draw.line(screen, GRAY, (10, y), (WIDTH - 10, y))
            y += 6

            for rank, uname, score, level, date in rows:
                row_color = YELLOW if rank == 1 else WHITE
                vals = [str(rank), uname[:12], str(score), str(level), date]
                for vx, vt in zip(col_x, vals):
                    surf = font_sm.render(vt, True, row_color)
                    screen.blit(surf, (vx, y))
                y += 28

        draw_button(screen, btn_back, "BACK", font_mid,
                    fill=(80, 30, 30), hover=mouse_hover(btn_back))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_b):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    return

        clock.tick(60)


def settings_screen(screen, clock, settings: dict):
    font_big = _font(32)
    font_mid = _font(20)

    COLOR_OPTIONS = [
        ("Green",  [100, 220, 100]),
        ("Blue",   [80,  160, 255]),
        ("Red",    [255, 80,  80]),
        ("Yellow", [255, 220, 0]),
        ("Purple", [180, 80,  220]),
    ]

    def current_color_name():
        c = settings.get("snake_color", [100, 220, 100])
        for name, val in COLOR_OPTIONS:
            if val == c:
                return name
        return "Custom"

    btn_color  = pygame.Rect(WIDTH // 2 - 130, 160, 260, 44)
    btn_grid   = pygame.Rect(WIDTH // 2 - 130, 220, 260, 44)
    btn_sound  = pygame.Rect(WIDTH // 2 - 130, 280, 260, 44)
    btn_save   = pygame.Rect(WIDTH // 2 - 130, 360, 260, 44)

    while True:
        screen.fill((15, 20, 35))
        text_center(screen, "SETTINGS", 50, font_big, CYAN)

        color_name = current_color_name()
        grid_val   = "ON" if settings.get("grid",  False) else "OFF"
        sound_val  = "ON" if settings.get("sound", True)  else "OFF"

        draw_button(screen, btn_color, f"Snake Color: {color_name}", font_mid,
                    hover=mouse_hover(btn_color))
        draw_button(screen, btn_grid,  f"Grid Overlay: {grid_val}", font_mid,
                    hover=mouse_hover(btn_grid))
        draw_button(screen, btn_sound, f"Sound: {sound_val}", font_mid,
                    hover=mouse_hover(btn_sound))
        draw_button(screen, btn_save,  "SAVE & BACK", font_mid,
                    fill=(30, 120, 30), hover=mouse_hover(btn_save))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_b):
                    save_settings(settings)
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_color.collidepoint(event.pos):
                    names = [n for n, _ in COLOR_OPTIONS]
                    cur   = current_color_name()
                    idx   = names.index(cur) if cur in names else 0
                    _, new_color = COLOR_OPTIONS[(idx + 1) % len(COLOR_OPTIONS)]
                    settings["snake_color"] = new_color
                elif btn_grid.collidepoint(event.pos):
                    settings["grid"] = not settings.get("grid", False)
                elif btn_sound.collidepoint(event.pos):
                    settings["sound"] = not settings.get("sound", True)
                elif btn_save.collidepoint(event.pos):
                    save_settings(settings)
                    return

        clock.tick(60)


def game_over_screen(screen, clock, result: dict, personal_best: int):
    font_big = _font(38)
    font_mid = _font(22)

    score   = result["score"]
    level   = result["level"]
    is_best = score >= personal_best and score > 0

    btn_retry = pygame.Rect(WIDTH // 2 - 130, 330, 260, 44)
    btn_menu  = pygame.Rect(WIDTH // 2 - 130, 385, 260, 44)

    while True:
        screen.fill((20, 10, 10))
        text_center(screen, "GAME OVER", 60, font_big, RED)

        text_center(screen, f"Score:  {score}",         145, font_mid)
        text_center(screen, f"Level:  {level}",         178, font_mid)
        text_center(screen, f"Best:   {personal_best}", 211, font_mid, YELLOW)

        if is_best:
            text_center(screen, "New Personal Best!", 255, font_mid, YELLOW)

        draw_button(screen, btn_retry, "R.  RETRY",     font_mid,
                    fill=(30, 120, 30), hover=mouse_hover(btn_retry))
        draw_button(screen, btn_menu,  "M.  MAIN MENU", font_mid,
                    fill=(70, 70, 70), hover=mouse_hover(btn_menu))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                if event.key in (pygame.K_m, pygame.K_ESCAPE):
                    return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(event.pos):
                    return "retry"
                if btn_menu.collidepoint(event.pos):
                    return "menu"

        clock.tick(60)


def main_menu(screen, clock):
    font_big = _font(42)
    font_mid = _font(22)

    btn_play  = pygame.Rect(WIDTH // 2 - 120, 200, 240, 48)
    btn_lb    = pygame.Rect(WIDTH // 2 - 120, 262, 240, 48)
    btn_set   = pygame.Rect(WIDTH // 2 - 120, 324, 240, 48)
    btn_quit  = pygame.Rect(WIDTH // 2 - 120, 386, 240, 48)

    while True:
        screen.fill((15, 20, 15))
        text_center(screen, "SNAKE", 80, font_big, GREEN)
        text_center(screen, "TSIS 4", 132, _font(20), GRAY)

        draw_button(screen, btn_play, "1.  PLAY",        font_mid, fill=(30, 130, 30), hover=mouse_hover(btn_play))
        draw_button(screen, btn_lb,   "2.  LEADERBOARD", font_mid, hover=mouse_hover(btn_lb))
        draw_button(screen, btn_set,  "3.  SETTINGS",    font_mid, hover=mouse_hover(btn_set))
        draw_button(screen, btn_quit, "Q.  QUIT",        font_mid, fill=(120, 30, 30), hover=mouse_hover(btn_quit))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  return "play"
                if event.key == pygame.K_2:  return "leaderboard"
                if event.key == pygame.K_3:  return "settings"
                if event.key == pygame.K_q:  pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.collidepoint(event.pos):   return "play"
                if btn_lb.collidepoint(event.pos):     return "leaderboard"
                if btn_set.collidepoint(event.pos):    return "settings"
                if btn_quit.collidepoint(event.pos):   pygame.quit(); sys.exit()

        clock.tick(60)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    pygame.init()
    pygame.mixer.init()

    screen   = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake — TSIS 4")
    clock    = pygame.time.Clock()
    settings = load_settings()

    username      = "Player"
    personal_best = 0

    while True:
        action = main_menu(screen, clock)

        if action == "leaderboard":
            leaderboard_screen(screen, clock)

        elif action == "settings":
            settings_screen(screen, clock, settings)

        elif action == "play":
            name = username_screen(screen, clock, username)
            if name is None:
                continue
            username = name

            if DB_OK:
                try:
                    personal_best = _db.get_personal_best(username)
                except Exception:
                    personal_best = 0

            while True:
                game   = SnakeGame(screen, settings, username, personal_best)
                result = game.run()

                if DB_OK:
                    try:
                        _db.save_session(username, result["score"], result["level"])
                        personal_best = _db.get_personal_best(username)
                    except Exception as e:
                        print(f"[DB] Save failed: {e}")

                choice = game_over_screen(screen, clock, result, personal_best)
                if choice == "menu":
                    break


if __name__ == "__main__":
    main()
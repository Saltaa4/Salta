import pygame


class UI:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 17)
        self.big_font = pygame.font.SysFont("Arial", 42)

        self.play_button = pygame.Rect(100, 220, 200, 42)
        self.leaderboard_button = pygame.Rect(100, 275, 200, 42)
        self.settings_button = pygame.Rect(100, 330, 200, 42)
        self.quit_button = pygame.Rect(100, 385, 200, 42)

        self.retry_button = pygame.Rect(75, 405, 250, 42)
        self.menu_button = pygame.Rect(75, 460, 250, 42)

        self.back_button = pygame.Rect(100, 520, 200, 42)

        self.settings_sound_button = pygame.Rect(60, 185, 280, 42)
        self.settings_color_button = pygame.Rect(60, 250, 280, 42)
        self.settings_difficulty_button = pygame.Rect(60, 315, 280, 42)

    def draw_text(self, text, x, y, color=(0, 0, 0), center=False, big=False, small=False):
        if big:
            font = self.big_font
        elif small:
            font = self.small_font
        else:
            font = self.font

        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y)) if center else surface.get_rect(topleft=(x, y))
        self.screen.blit(surface, rect)

    def draw_button(self, rect, text, fill=(210, 210, 210), text_color=(0, 0, 0)):
        pygame.draw.rect(self.screen, fill, rect, border_radius=8)
        pygame.draw.rect(self.screen, (30, 30, 30), rect, 2, border_radius=8)
        self.draw_text(text, rect.centerx, rect.centery, text_color, center=True)

    def draw_main_menu(self):
        self.screen.fill((225, 225, 225))

        self.draw_text("RACER PRO", self.width // 2, 140, (0, 0, 0), center=True, big=True)

        self.draw_button(self.play_button, "1. PLAY", (120, 220, 120))
        self.draw_button(self.leaderboard_button, "2. LEADERBOARD")
        self.draw_button(self.settings_button, "3. SETTINGS")
        self.draw_button(self.quit_button, "Q. QUIT", (220, 120, 120))

        self.draw_text("Use mouse or keyboard", self.width // 2, 545, (80, 80, 80), center=True, small=True)

        pygame.display.update()

    def draw_username_screen(self, username):
        self.screen.fill((235, 235, 235))

        self.draw_text("ENTER USERNAME", self.width // 2, 155, (0, 0, 0), center=True, big=True)

        input_rect = pygame.Rect(55, 260, 290, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), input_rect, border_radius=8)
        pygame.draw.rect(self.screen, (0, 0, 0), input_rect, 2, border_radius=8)

        self.draw_text(username + "|", self.width // 2, input_rect.centery, (0, 0, 0), center=True)

        self.draw_text("Enter = Start", self.width // 2, 370, (0, 120, 0), center=True)
        self.draw_text("Esc = Back", self.width // 2, 410, (150, 0, 0), center=True)

        pygame.display.update()

    def draw_leaderboard_screen(self, leaderboard):
        self.screen.fill((245, 245, 245))

        self.draw_text("TOP 10", self.width // 2, 45, (0, 0, 0), center=True, big=True)

        if not leaderboard:
            self.draw_text("No records yet", self.width // 2, 260, (100, 100, 100), center=True)
        else:
            y = 100
            self.draw_text("Rank   Name        Score   Dist", 28, y, (0, 0, 0), small=True)
            y += 30

            for i, entry in enumerate(leaderboard[:10], start=1):
                name = str(entry.get("name", "Player"))[:9]
                score = int(entry.get("score", 0))
                distance = int(entry.get("distance", 0))
                line = f"{i:>2}.    {name:<9} {score:<6} {distance}m"
                self.draw_text(line, 28, y, (40, 40, 40), small=True)
                y += 34

        self.draw_button(self.back_button, "B / ESC / BACK", (220, 220, 220))

        pygame.display.update()

    def draw_settings_screen(self, settings):
        self.screen.fill((235, 235, 235))

        self.draw_text("SETTINGS", self.width // 2, 90, (0, 0, 0), center=True, big=True)

        sound = "ON" if settings.get("sound", True) else "OFF"
        color = settings.get("car_color", "blue").upper()
        difficulty = settings.get("difficulty", "normal").upper()

        self.draw_button(self.settings_sound_button, f"1. SOUND: {sound}")
        self.draw_button(self.settings_color_button, f"2. CAR COLOR: {color}")
        self.draw_button(self.settings_difficulty_button, f"3. DIFFICULTY: {difficulty}")

        self.draw_text("Click buttons or press 1 / 2 / 3", self.width // 2, 405, (60, 60, 60), center=True, small=True)

        self.draw_button(self.back_button, "B / ESC / BACK", (220, 220, 220))

        pygame.display.update()

    def draw_game_over_screen(self, result):
        self.screen.fill((240, 240, 240))

        title = "FINISH!" if result.get("finished") else "GAME OVER"
        title_color = (0, 140, 0) if result.get("finished") else (180, 0, 0)

        self.draw_text(title, self.width // 2, 95, title_color, center=True, big=True)

        score = result.get("score", 0)
        distance = result.get("distance", 0)
        coins = result.get("coins", 0)

        self.draw_text(f"Score: {score}", self.width // 2, 190, (0, 0, 0), center=True)
        self.draw_text(f"Distance: {distance}m", self.width // 2, 230, (0, 0, 0), center=True)
        self.draw_text(f"Coins: {coins}", self.width // 2, 270, (0, 0, 0), center=True)

        self.draw_button(self.retry_button, "R. RETRY", (120, 220, 120))
        self.draw_button(self.menu_button, "M. MAIN MENU", (220, 220, 220))

        pygame.display.update()
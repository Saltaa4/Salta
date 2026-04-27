# game.py
import pygame
import random
import os
from config import *


BASE_DIR = os.path.dirname(__file__)


def _img(name):
    return os.path.join(BASE_DIR, "assets", "images", name)

def _snd(name):
    return os.path.join(BASE_DIR, "assets", "sounds", name)


# ── Helpers ───────────────────────────────────────────────────────────────────

def random_cell(exclude: set) -> tuple:
    """Return a random (col, row) not in exclude."""
    while True:
        c = random.randint(0, COLS - 1)
        r = random.randint(0, ROWS - 1)
        if (c, r) not in exclude:
            return (c, r)


def cell_to_px(cell):
    return (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE)


# ── Game class ────────────────────────────────────────────────────────────────

class SnakeGame:
    """
    Returns result dict from run() when game ends:
      {"score": int, "level": int}
    """

    def __init__(self, screen, settings: dict, username: str, personal_best: int):
        self.screen   = screen
        self.settings = settings
        self.username = username
        self.best     = personal_best

        self.clock = pygame.time.Clock()
        self.font  = pygame.font.SysFont("Arial", 20)
        self.small = pygame.font.SysFont("Arial", 15)

        self._load_assets()
        self._load_sounds()
        self._init_state()

    # ── Asset loading ─────────────────────────────────────────────────────────

    def _load_assets(self):
        def load(name, size=(CELL_SIZE, CELL_SIZE)):
            img = pygame.image.load(_img(name)).convert_alpha()
            return pygame.transform.smoothscale(img, size)

        self.bg_img       = pygame.transform.smoothscale(
            pygame.image.load(_img("background.png")).convert(), (WIDTH, HEIGHT))
        self.snake_img    = load("snake.png")
        self.food_img     = load("food.png")
        self.poison_img   = load("poison.png")
        self.pu_shield    = load("powerup_shield.png")
        self.pu_slow      = load("powerup_slow.png")
        self.pu_speed     = load("powerup_speed.png")

        # One tinted snake image used for ALL segments
        color = tuple(self.settings.get("snake_color", [100, 220, 100]))
        self.snake_tinted = self.snake_img.copy()
        self.snake_tinted.fill(color, special_flags=pygame.BLEND_RGB_MULT)

    def _load_sounds(self):
        self.sound_on = self.settings.get("sound", True)
        self.snd_eat   = None
        self.snd_music = None
        if not self.sound_on:
            return
        try:
            self.snd_eat = pygame.mixer.Sound(_snd("eating.mp3"))
            self.snd_eat.set_volume(0.6)
        except Exception:
            pass
        try:
            pygame.mixer.music.load(_snd("super-mario-bros-2.mp3"))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    # ── State init ────────────────────────────────────────────────────────────

    def _init_state(self):
        mid = (COLS // 2, ROWS // 2)
        self.snake     = [mid, (mid[0]-1, mid[1]), (mid[0]-2, mid[1])]
        self.direction = (1, 0)
        self.next_dir  = (1, 0)

        self.score = 0
        self.level = 1
        self.foods_eaten = 0

        self.obstacles: set = set()

        # poison и powerup объявляем ДО _spawn_food — она их использует
        self.poison      = None
        self.poison_born = 0
        self._poison_timer = pygame.time.get_ticks() + random.randint(8000, 15000)

        self.powerup   = None
        self._pu_timer = pygame.time.get_ticks() + random.randint(10000, 20000)

        # food — спавним последним
        self.food      = None
        self.food_w    = 1
        self.food_born = 0
        self._spawn_food()

        # active effect
        self.effect         = None   # "speed" | "slow" | "shield"
        self.effect_end     = 0

        self.shield_ready   = False  # shield collected, waiting to absorb hit

        # speed
        self._base_fps = BASE_SPEED + (self.level - 1) * SPEED_PER_LEVEL
        self._move_acc = 0.0         # fractional frame accumulator

        self.game_over = False

    # ── Spawn helpers ─────────────────────────────────────────────────────────

    def _occupied(self):
        return set(self.snake) | self.obstacles

    def _spawn_food(self):
        exclude = self._occupied()
        if self.poison:
            exclude.add(self.poison)
        if self.powerup:
            exclude.add(self.powerup["cell"])
        self.food      = random_cell(exclude)
        self.food_w    = random.choice([1, 1, 2, 2, 3])
        self.food_born = pygame.time.get_ticks()

    def _maybe_spawn_poison(self, now):
        if self.poison is None and now >= self._poison_timer:
            exclude = self._occupied() | ({self.food} if self.food else set())
            self.poison      = random_cell(exclude)
            self.poison_born = now
            self._poison_timer = now + random.randint(12000, 20000)

    def _maybe_spawn_powerup(self, now):
        if self.powerup is None and now >= self._pu_timer:
            kind = random.choice(["speed", "slow", "shield"])
            img  = {"speed": self.pu_speed, "slow": self.pu_slow, "shield": self.pu_shield}[kind]
            exclude = self._occupied() | ({self.food} if self.food else set())
            if self.poison:
                exclude.add(self.poison)
            cell = random_cell(exclude)
            self.powerup = {"kind": kind, "born": now, "cell": cell, "img": img}
            self._pu_timer = now + random.randint(15000, 25000)

    def _spawn_obstacles(self):
        """Add OBSTACLES_PER_LEVEL new blocks that don't trap the snake head."""
        head = self.snake[0]
        forbidden = self._occupied()
        # keep 3-cell radius around head clear
        safe_zone = {(head[0]+dc, head[1]+dr)
                     for dc in range(-3, 4) for dr in range(-3, 4)}
        forbidden |= safe_zone
        added = 0
        attempts = 0
        while added < OBSTACLES_PER_LEVEL and attempts < 500:
            attempts += 1
            c = random.randint(0, COLS - 1)
            r = random.randint(0, ROWS - 1)
            cell = (c, r)
            if cell not in forbidden:
                self.obstacles.add(cell)
                forbidden.add(cell)
                added += 1

    # ── Speed ─────────────────────────────────────────────────────────────────

    def _current_fps(self):
        fps = BASE_SPEED + (self.level - 1) * SPEED_PER_LEVEL
        if self.effect == "speed":
            fps = int(fps * SPEED_BOOST_MULT)
        elif self.effect == "slow":
            fps = max(2, int(fps * SLOW_MOTION_MULT))
        return fps

    # ── Core update ───────────────────────────────────────────────────────────

    def _step(self):
        """Move snake one cell. Returns False if game over."""
        self.direction = self.next_dir
        head = (self.snake[0][0] + self.direction[0],
                self.snake[0][1] + self.direction[1])

        # Wall collision
        if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
            if self.shield_ready:
                self.shield_ready = False
                self.effect = None
                return True  # выжили, змея не двигается в этот шаг
            return False

        # Obstacle collision
        if head in self.obstacles:
            print(f"[DEBUG] Hit obstacle! shield_ready={self.shield_ready}")
            if self.shield_ready:
                self.shield_ready = False
                self.effect = None
                print("[DEBUG] Shield saved you!")
                return True
            return False

        # Self collision
        if head in self.snake:
            if self.shield_ready:
                self.shield_ready = False
                self.effect = None
                return True
            return False

        self.snake.insert(0, head)

        # Eat food
        if head == self.food:
            self.score      += FOOD_SCORE.get(self.food_w, 1)
            self.foods_eaten += 1
            if self.sound_on and self.snd_eat:
                self.snd_eat.play()
            self._spawn_food()

            # Level up
            if self.foods_eaten % FOOD_PER_LEVEL == 0:
                self.level += 1
                if self.level >= OBSTACLE_START_LEVEL:
                    self._spawn_obstacles()
        else:
            self.snake.pop()

        # Eat poison
        if head == self.poison:
            self.poison = None
            # shorten by 2
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            if len(self.snake) <= 1:
                return False

        # Collect power-up
        if self.powerup and head == self.powerup["cell"]:
            kind = self.powerup["kind"]
            self.powerup = None
            if kind == "shield":
                self.effect       = "shield"
                self.shield_ready = True
                self.effect_end   = pygame.time.get_ticks() + 99999
            else:
                # НЕ сбрасываем shield_ready если щит уже активен
                self.effect     = kind
                self.effect_end = pygame.time.get_ticks() + POWERUP_EFFECT_DURATION
                # shield_ready не трогаем!

        return True

    # ── Draw ──────────────────────────────────────────────────────────────────

    def _draw(self, now):
        self.screen.blit(self.bg_img, (0, 0))

        # Grid
        if self.settings.get("grid", False):
            for c in range(COLS):
                pygame.draw.line(self.screen, (60, 60, 60),
                                 (c * CELL_SIZE, 0), (c * CELL_SIZE, HEIGHT))
            for r in range(ROWS):
                pygame.draw.line(self.screen, (60, 60, 60),
                                 (0, r * CELL_SIZE), (WIDTH, r * CELL_SIZE))

        # Obstacles
        for cell in self.obstacles:
            pygame.draw.rect(self.screen, GRAY,
                             (*cell_to_px(cell), CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, DARK_GRAY,
                             (*cell_to_px(cell), CELL_SIZE, CELL_SIZE), 2)

        # Food
        if self.food:
            colors = {1: GREEN, 2: YELLOW, 3: RED}
            tinted = self.food_img.copy()
            tinted.fill(colors[self.food_w], special_flags=pygame.BLEND_RGB_MULT)
            self.screen.blit(tinted, cell_to_px(self.food))
            # timer bar
            elapsed = now - self.food_born
            frac    = max(0, 1 - elapsed / FOOD_LIFETIME)
            bar_w   = int(CELL_SIZE * frac)
            pygame.draw.rect(self.screen, YELLOW,
                             (cell_to_px(self.food)[0], cell_to_px(self.food)[1] - 4,
                              bar_w, 3))

        # Poison
        if self.poison:
            self.screen.blit(self.poison_img, cell_to_px(self.poison))

        # Power-up
        if self.powerup:
            self.screen.blit(self.powerup["img"], cell_to_px(self.powerup["cell"]))
            # disappear timer bar
            elapsed = now - self.powerup["born"]
            frac    = max(0, 1 - elapsed / POWERUP_FIELD_LIFETIME)
            bar_w   = int(CELL_SIZE * frac)
            px = cell_to_px(self.powerup["cell"])
            pygame.draw.rect(self.screen, CYAN, (px[0], px[1] - 4, bar_w, 3))

        # Snake — every segment is the same tinted image rotated by direction
        dx, dy = self.direction
        if   (dx, dy) == (1,  0): angle = 0
        elif (dx, dy) == (-1, 0): angle = 180
        elif (dx, dy) == (0, -1): angle = 90
        else:                     angle = 270
        seg_img = pygame.transform.rotate(self.snake_tinted, angle)
        seg_img = pygame.transform.smoothscale(seg_img, (CELL_SIZE, CELL_SIZE))
        for seg in self.snake:
            self.screen.blit(seg_img, cell_to_px(seg))

        # HUD
        self._draw_hud(now)

        pygame.display.update()

    def _draw_hud(self, now):
        lines = [
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Best:  {self.best}",
            f"User:  {self.username}",
        ]
        y = 6
        for line in lines:
            surf = self.font.render(line, True, WHITE)
            # dark bg for readability
            pygame.draw.rect(self.screen, (0, 0, 0, 160),
                             (6, y, surf.get_width() + 4, surf.get_height()))
            self.screen.blit(surf, (8, y))
            y += surf.get_height() + 2

        # Active effect
        if self.effect:
            if self.effect == "shield":
                label = "🛡 Shield READY"
                col   = CYAN
            elif self.effect == "speed":
                rem   = max(0, (self.effect_end - now) // 1000)
                label = f"⚡ Speed {rem}s"
                col   = ORANGE
            else:
                rem   = max(0, (self.effect_end - now) // 1000)
                label = f"🐢 Slow {rem}s"
                col   = BLUE
            surf = self.font.render(label, True, col)
            self.screen.blit(surf, (WIDTH - surf.get_width() - 8, 8))

        # Food weight info (bottom right)
        info = self.small.render(
            f"Food ×{self.food_w}  ({FOOD_SCORE.get(self.food_w,1)} pts)", True, YELLOW)
        self.screen.blit(info, (WIDTH - info.get_width() - 8, HEIGHT - 22))

    # ── Main loop ─────────────────────────────────────────────────────────────

    def run(self) -> dict:
        dt_acc = 0.0   # ms accumulator for snake steps

        while True:
            dt  = self.clock.tick(FPS)
            now = pygame.time.get_ticks()

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    dx, dy = self.direction
                    if event.key == pygame.K_UP    and dy == 0:
                        self.next_dir = (0, -1)
                    elif event.key == pygame.K_DOWN  and dy == 0:
                        self.next_dir = (0,  1)
                    elif event.key == pygame.K_LEFT  and dx == 0:
                        self.next_dir = (-1, 0)
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        self.next_dir = (1,  0)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return {"score": self.score, "level": self.level}

            # Expire effect
            if self.effect and self.effect != "shield" and now >= self.effect_end:
                self.effect = None

            # Expire food
            if self.food and now - self.food_born > FOOD_LIFETIME:
                self._spawn_food()

            # Expire poison
            if self.poison and now - self.poison_born > POISON_LIFETIME:
                self.poison = None

            # Expire power-up on field
            if self.powerup and now - self.powerup["born"] > POWERUP_FIELD_LIFETIME:
                self.powerup = None

            # Spawn poison / power-up
            self._maybe_spawn_poison(now)
            self._maybe_spawn_powerup(now)

            # Move snake at its own pace
            ms_per_step = 1000 / self._current_fps()
            dt_acc += dt
            if dt_acc >= ms_per_step:
                dt_acc -= ms_per_step
                alive = self._step()
                if not alive:
                    pygame.mixer.music.stop()
                    self._draw(now)
                    return {"score": self.score, "level": self.level}

            self._draw(now)
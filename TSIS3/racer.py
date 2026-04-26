import random
from pathlib import Path

import pygame


LANES = [80, 160, 240, 320]


def load_image(path, size=None):
    image = pygame.image.load(str(path)).convert_alpha()
    if size:
        image = pygame.transform.smoothscale(image, size)
    return image


def tint_surface(surface, color_name):
    color_map = {
        "blue": (255, 255, 255),
        "red": (255, 80, 80),
        "green": (80, 255, 120),
        "yellow": (255, 255, 80),
    }

    tint = color_map.get(color_name, (255, 255, 255))
    result = surface.copy()
    result.fill(tint, special_flags=pygame.BLEND_RGB_MULT)
    return result


def load_game_assets(base_dir, width, height):
    img_dir = base_dir / "assets" / "images"

    assets = {
        "road": pygame.transform.smoothscale(
            pygame.image.load(str(img_dir / "background.png")).convert(),
            (width, height)
        ),
        "player": load_image(img_dir / "player_car.png", (56, 86)),
        "enemy": load_image(img_dir / "enemy_car.png", (56, 86)),
        "coin": load_image(img_dir / "coin.png", (32, 32)),
        "barrier": load_image(img_dir / "road_block_barrier.png", (70, 38)),
        "oil": load_image(img_dir / "oil.png", (46, 46)),
        "nitro": load_image(img_dir / "nitro.png", (34, 46)),
        "shield": load_image(img_dir / "shield.png", (40, 40)),
        "repair": load_image(img_dir / "repair.png", (40, 40)),
    }

    return assets


class FallingObject:
    def __init__(self, kind, image, x, y, speed, value=0, timeout=7.0):
        self.kind = kind
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.value = value
        self.spawn_time = pygame.time.get_ticks()
        self.timeout = timeout
        self.move_dir = random.choice([-1, 1])
        self.move_timer = random.randint(30, 90)

    def update(self, road_speed):
        self.rect.y += self.speed + road_speed

        if self.kind == "moving_barrier":
            self.rect.x += self.move_dir * 2
            self.move_timer -= 1

            if self.rect.left < 45 or self.rect.right > 355:
                self.move_dir *= -1

            if self.move_timer <= 0:
                self.move_dir *= -1
                self.move_timer = random.randint(30, 90)

    def expired(self, height):
        lifetime = (pygame.time.get_ticks() - self.spawn_time) / 1000
        return self.rect.top > height or lifetime > self.timeout


class RacerGame:
    def __init__(self, screen, assets, sounds, settings):
        self.screen = screen
        self.assets = assets
        self.sounds = sounds
        self.settings = settings

        self.width = screen.get_width()
        self.height = screen.get_height()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 16)

        self.road_y = 0

        self.player_image = tint_surface(
            self.assets["player"],
            self.settings.get("car_color", "blue")
        )
        self.player_rect = self.player_image.get_rect(center=(self.width // 2, self.height - 95))

        self.difficulty = self.settings.get("difficulty", "normal")
        self.base_speed = {"easy": 4, "normal": 5, "hard": 6}.get(self.difficulty, 5)
        self.finish_distance = {"easy": 1000, "normal": 1500, "hard": 2000}.get(self.difficulty, 1500)

        self.player_move_speed = 6
        self.road_speed = self.base_speed

        self.traffic = []
        self.obstacles = []
        self.coins = []
        self.powerups = []

        self.coins_count = 0
        self.coin_score = 0
        self.power_bonus = 0
        self.distance = 0

        self.active_power = None
        self.power_end_time = 0
        self.has_shield = False
        self.oil_slow_until = 0

        self.spawn_enemy_timer = 0
        self.spawn_coin_timer = 0
        self.spawn_obstacle_timer = 0
        self.spawn_powerup_timer = 0

        self.game_over = False

    def sound_enabled(self):
        return self.settings.get("sound", True)

    def play_sound(self, name):
        if not self.sound_enabled():
            return
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def current_score(self):
        return self.coin_score * 10 + int(self.distance * 0.5) + self.power_bonus

    def difficulty_level(self):
        return min(8, int(self.distance // 250))

    def choose_lane_x(self):
        return random.choice(LANES)

    def lane_is_safe(self, x, y=-80):
        candidate = pygame.Rect(0, 0, 60, 90)
        candidate.center = (x, y)

        all_objects = self.traffic + self.obstacles + self.coins + self.powerups

        for obj in all_objects:
            if candidate.inflate(20, 80).colliderect(obj.rect):
                return False

        return True

    def get_safe_spawn_x(self):
        lanes = LANES[:]
        random.shuffle(lanes)

        for x in lanes:
            if self.lane_is_safe(x):
                return x

        return random.choice(LANES)

    def spawn_enemy(self):
        x = self.get_safe_spawn_x()
        speed = 1 + self.difficulty_level() * 0.15
        self.traffic.append(FallingObject("traffic", self.assets["enemy"], x, -80, speed, timeout=12))

    def spawn_coin(self):
        x = self.get_safe_spawn_x()
        weight = random.choice([1, 1, 1, 2, 2, 3])
        self.coins.append(FallingObject("coin", self.assets["coin"], x, -40, 0, value=weight, timeout=8))

    def spawn_obstacle(self):
        x = self.get_safe_spawn_x()
        kind = random.choice(["barrier", "oil", "moving_barrier"])

        if kind in ("barrier", "moving_barrier"):
            image = self.assets["barrier"]
        else:
            image = self.assets["oil"]

        self.obstacles.append(FallingObject(kind, image, x, -45, 0, timeout=9))

    def spawn_powerup(self):
        if self.active_power is not None:
            return

        x = self.get_safe_spawn_x()
        kind = random.choice(["Nitro", "Shield", "Repair"])

        image = {
            "Nitro": self.assets["nitro"],
            "Shield": self.assets["shield"],
            "Repair": self.assets["repair"],
        }[kind]

        self.powerups.append(FallingObject(kind, image, x, -45, 0, timeout=7))

    def handle_spawning(self):
        level = self.difficulty_level()

        self.spawn_enemy_timer -= 1
        self.spawn_coin_timer -= 1
        self.spawn_obstacle_timer -= 1
        self.spawn_powerup_timer -= 1

        if self.spawn_enemy_timer <= 0:
            self.spawn_enemy()
            self.spawn_enemy_timer = max(35, 95 - level * 7)

        if self.spawn_coin_timer <= 0:
            self.spawn_coin()
            self.spawn_coin_timer = max(30, 70 - level * 3)

        if self.spawn_obstacle_timer <= 0:
            self.spawn_obstacle()
            self.spawn_obstacle_timer = max(45, 120 - level * 6)

        if self.spawn_powerup_timer <= 0:
            self.spawn_powerup()
            self.spawn_powerup_timer = random.randint(300, 480)

    def update_road(self):
        speed = self.road_speed

        if self.active_power == "Nitro":
            speed += 3

        if pygame.time.get_ticks() < self.oil_slow_until:
            speed = max(2, speed - 2)

        self.road_y = (self.road_y + speed) % self.height
        self.distance += speed / 18

    def update_player(self):
        keys = pygame.key.get_pressed()

        move_speed = self.player_move_speed

        if self.active_power == "Nitro":
            move_speed += 2

        if pygame.time.get_ticks() < self.oil_slow_until:
            move_speed = max(3, move_speed - 2)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_rect.x -= move_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_rect.x += move_speed

        road_left = 35
        road_right = self.width - 35

        if self.player_rect.left < road_left:
            self.player_rect.left = road_left

        if self.player_rect.right > road_right:
            self.player_rect.right = road_right

    def update_objects(self):
        for group in [self.traffic, self.obstacles, self.coins, self.powerups]:
            for obj in group[:]:
                obj.update(self.road_speed)
                if obj.expired(self.height):
                    group.remove(obj)

    def update_power_timer(self):
        now = pygame.time.get_ticks()

        if self.active_power == "Nitro" and now >= self.power_end_time:
            self.active_power = None
            self.power_end_time = 0

    def activate_powerup(self, power_type):
        now = pygame.time.get_ticks()

        if power_type == "Repair":
            if self.obstacles:
                nearest = max(self.obstacles, key=lambda obj: obj.rect.y)
                self.obstacles.remove(nearest)
            self.power_bonus += 25
            self.play_sound("powerup")
            return

        if self.active_power is not None:
            return

        if power_type == "Nitro":
            self.active_power = "Nitro"
            self.power_end_time = now + 4000
            self.power_bonus += 20
            self.play_sound("powerup")

        elif power_type == "Shield":
            self.active_power = "Shield"
            self.has_shield = True
            self.power_bonus += 15
            self.play_sound("powerup")

    def handle_crash(self):
        if self.has_shield:
            self.has_shield = False
            self.active_power = None
            self.power_end_time = 0
            self.play_sound("collision")
            return False

        self.play_sound("fail")
        return True

    def handle_collisions(self):
        for enemy in self.traffic[:]:
            if self.player_rect.colliderect(enemy.rect):
                if self.handle_crash():
                    return True
                self.traffic.remove(enemy)

        for obstacle in self.obstacles[:]:
            if self.player_rect.colliderect(obstacle.rect):
                if obstacle.kind in ["barrier", "moving_barrier"]:
                    if self.handle_crash():
                        return True
                    self.obstacles.remove(obstacle)

                elif obstacle.kind == "oil":
                    self.oil_slow_until = pygame.time.get_ticks() + 2000
                    self.obstacles.remove(obstacle)

        for coin in self.coins[:]:
            if self.player_rect.colliderect(coin.rect):
                self.coins_count += 1
                self.coin_score += coin.value
                self.coins.remove(coin)
                self.play_sound("click")

                self.road_speed = self.base_speed + self.coin_score // 10

        for power in self.powerups[:]:
            if self.player_rect.colliderect(power.rect):
                self.activate_powerup(power.kind)
                self.powerups.remove(power)

        return False

    def draw_road(self):
        self.screen.blit(self.assets["road"], (0, self.road_y - self.height))
        self.screen.blit(self.assets["road"], (0, self.road_y))

    def draw_hud(self):
        score = self.current_score()
        remaining = max(0, int(self.finish_distance - self.distance))

        texts = [
            f"Score: {score}",
            f"Coins: {self.coins_count}",
            f"Dist: {int(self.distance)}m",
            f"Left: {remaining}m",
        ]

        x = 8
        y = 8

        for text in texts:
            rendered = self.small_font.render(text, True, (255, 255, 255))
            self.screen.blit(rendered, (x, y))
            y += 20

        if self.active_power:
            if self.active_power == "Nitro":
                remaining_time = max(0, (self.power_end_time - pygame.time.get_ticks()) // 1000)
                power_text = f"Power: Nitro {remaining_time}s"
            else:
                power_text = "Power: Shield ready"

            rendered = self.small_font.render(power_text, True, (255, 255, 0))
            self.screen.blit(rendered, (8, 90))

    def draw(self):
        self.draw_road()

        for obj in self.coins:
            self.screen.blit(obj.image, obj.rect)

            if obj.value > 1:
                value_text = self.small_font.render(str(obj.value), True, (0, 0, 0))
                value_rect = value_text.get_rect(center=obj.rect.center)
                self.screen.blit(value_text, value_rect)

        for obj in self.obstacles:
            self.screen.blit(obj.image, obj.rect)

        for obj in self.powerups:
            self.screen.blit(obj.image, obj.rect)

        for obj in self.traffic:
            self.screen.blit(obj.image, obj.rect)

        self.screen.blit(self.player_image, self.player_rect)
        self.draw_hud()

    def result(self, finished=False):
        return {
            "score": self.current_score(),
            "distance": int(self.distance),
            "coins": self.coins_count,
            "finished": finished,
        }

    def run_frame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.result(finished=False)

        self.update_road()
        self.update_player()
        self.handle_spawning()
        self.update_objects()
        self.update_power_timer()

        crashed = self.handle_collisions()

        self.draw()
        pygame.display.update()

        if crashed:
            return self.result(finished=False)

        if self.distance >= self.finish_distance:
            self.power_bonus += 100
            return self.result(finished=True)

        return None
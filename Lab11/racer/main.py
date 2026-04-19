import pygame
import random
import sys
import os

pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Clock for FPS
clock = pygame.time.Clock()

# Change working directory to script folder
os.chdir(os.path.dirname(__file__))

# Load images
road = pygame.image.load("png/background.png")
car = pygame.image.load("png/player.png")
enemy = pygame.image.load("png/enemy.png")
coin = pygame.image.load("png/coin.png")

# Resize images
road = pygame.transform.scale(road, (WIDTH, HEIGHT))
car = pygame.transform.scale(car, (50, 100))
enemy = pygame.transform.scale(enemy, (50, 100))
coin = pygame.transform.scale(coin, (30, 30))

# Player settings
player_rect = car.get_rect(center=(WIDTH // 2, HEIGHT - 100))

# Enemy settings
enemy_rect = enemy.get_rect(center=(WIDTH // 2, -100))
enemy_speed = 5

# Coin settings
coin_rect = coin.get_rect(center=(random.randint(50, WIDTH - 50), -50))
coin_speed = 5

# Score settings
coins_collected = 0
coin_weight = 1

# Increase enemy speed after every N points
N = 5

# Font for score text
font = pygame.font.SysFont("Arial", 24)

def respawn_coin():
    """Create a new random coin position and assign a random weight."""
    x = random.randint(50, WIDTH - 50)
    y = -50
    weight = random.choice([1, 2, 3])
    return pygame.Rect(x, y, 30, 30), weight

def get_coin_color(weight):
    """Return a different color based on coin weight."""
    if weight == 1:
        return BRONZE
    elif weight == 2:
        return SILVER
    return GOLD

# Initial random coin
coin_rect, coin_weight = respawn_coin()

running = True
while running:
    screen.blit(road, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += 5

    # Enemy movement
    enemy_rect.y += enemy_speed
    if enemy_rect.top > HEIGHT:
        enemy_rect.center = (random.randint(50, WIDTH - 50), -100)

    # Coin movement
    coin_rect.y += coin_speed
    if coin_rect.top > HEIGHT:
        coin_rect, coin_weight = respawn_coin()

    # Collision with enemy
    if player_rect.colliderect(enemy_rect):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Collision with coin
    if player_rect.colliderect(coin_rect):
        coins_collected += coin_weight
        coin_rect, coin_weight = respawn_coin()

        # Increase enemy speed each time player reaches the next threshold
        enemy_speed = 5 + (coins_collected // N)

    # Draw player and enemy
    screen.blit(car, player_rect)
    screen.blit(enemy, enemy_rect)

    # Draw coin with color depending on its weight
    coin_copy = coin.copy()
    tinted_coin = coin.copy()
    tinted_coin.fill(get_coin_color(coin_weight), special_flags=pygame.BLEND_RGB_MULT)
    screen.blit(tinted_coin, coin_rect)

    # Draw score and speed info
    score_text = font.render(f"Coins: {coins_collected}", True, BLACK)
    weight_text = font.render(f"Weight: {coin_weight}", True, BLACK)
    speed_text = font.render(f"Enemy speed: {enemy_speed}", True, BLACK)

    screen.blit(score_text, (WIDTH - 140, 20))
    screen.blit(weight_text, (10, 20))
    screen.blit(speed_text, (10, 50))

    pygame.display.update()
    clock.tick(60)
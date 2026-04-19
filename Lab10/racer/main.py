import pygame, random, sys, os

pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
coins_collected = 0

# Font for score
font = pygame.font.SysFont("Arial", 24)

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
        coin_rect.center = (random.randint(50, WIDTH - 50), -50)

    # Collision with enemy
    if player_rect.colliderect(enemy_rect):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Collision with coin
    if player_rect.colliderect(coin_rect):
        coins_collected += 1
        coin_rect.center = (random.randint(50, WIDTH - 50), -50)

    # Draw objects
    screen.blit(car, player_rect)
    screen.blit(enemy, enemy_rect)
    screen.blit(coin, coin_rect)

    # Draw score
    score_text = font.render(f"Coins: {coins_collected}", True, BLACK)
    screen.blit(score_text, (WIDTH - 120, 20))

    pygame.display.update()
    clock.tick(60)
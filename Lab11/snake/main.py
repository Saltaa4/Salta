import pygame
import random
import sys
import os

pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Images")

# Colors
WHITE = (255, 255, 255)
RED = (255, 80, 80)
YELLOW = (255, 220, 0)
GREEN = (100, 255, 100)

# Clock
clock = pygame.time.Clock()

# Fix path
os.chdir(os.path.dirname(__file__))

# Load images
background = pygame.image.load("png/background.png")
snake_img = pygame.image.load("png/snake.png")
food_img = pygame.image.load("png/food.png")

# Resize images
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
snake_img = pygame.transform.scale(snake_img, (CELL_SIZE, CELL_SIZE))
food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))

# Snake setup
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)

# Font
font = pygame.font.SysFont("Arial", 24)

# Game variables
score = 0
speed = 10

# Food settings
food = None
food_weight = 1
food_spawn_time = 0
FOOD_LIFETIME = 5000  # milliseconds

def random_food():
    """Generate food at a random position that is not on the snake."""
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

def spawn_food():
    """Create new food with random weight and remember spawn time."""
    position = random_food()
    weight = random.choice([1, 2, 3])
    spawn_time = pygame.time.get_ticks()
    return position, weight, spawn_time

def get_food_color(weight):
    """Return color depending on food weight."""
    if weight == 1:
        return GREEN
    elif weight == 2:
        return YELLOW
    return RED

# Initial food
food, food_weight, food_spawn_time = spawn_food()

running = True
while running:
    screen.blit(background, (0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
        direction = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
        direction = (0, CELL_SIZE)
    if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
        direction = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
        direction = (CELL_SIZE, 0)

    # New head position
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Wall collision
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        print("Game Over! Hit wall")
        pygame.quit()
        sys.exit()

    # Self collision
    if new_head in snake:
        print("Game Over! Hit itself")
        pygame.quit()
        sys.exit()

    # Move snake
    snake.insert(0, new_head)

    # Check if food expired
    current_time = pygame.time.get_ticks()
    if current_time - food_spawn_time > FOOD_LIFETIME:
        food, food_weight, food_spawn_time = spawn_food()

    # Eat food
    if new_head == food:
        score += food_weight
        food, food_weight, food_spawn_time = spawn_food()
    else:
        snake.pop()

    # Rotate the snake based on its current direction
    if direction == (CELL_SIZE, 0):        # moving right
        current_snake_img = snake_img
    elif direction == (-CELL_SIZE, 0):     # moving left
        current_snake_img = pygame.transform.flip(snake_img, True, False)
    elif direction == (0, -CELL_SIZE):     # moving up
        current_snake_img = pygame.transform.rotate(snake_img, 90)
    elif direction == (0, CELL_SIZE):      # moving down
        current_snake_img = pygame.transform.rotate(snake_img, -90)

    # Draw snake
    for segment in snake:
        screen.blit(current_snake_img, segment)

    # Draw food with color depending on weight
    tinted_food = food_img.copy()
    tinted_food.fill(get_food_color(food_weight), special_flags=pygame.BLEND_RGB_MULT)
    screen.blit(tinted_food, food)

    # Show timer for disappearing food
    time_left = max(0, (FOOD_LIFETIME - (current_time - food_spawn_time)) // 1000 + 1)

    # Draw score and food info
    score_text = font.render(f"Score: {score}", True, WHITE)
    weight_text = font.render(f"Food weight: {food_weight}", True, WHITE)
    timer_text = font.render(f"Food timer: {time_left}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(weight_text, (10, 40))
    screen.blit(timer_text, (WIDTH - 170, 10))

    pygame.display.update()
    clock.tick(speed)
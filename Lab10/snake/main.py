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

# Generate food (not on snake)
def random_food():
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

food = random_food()

# Game variables
score = 0
level = 1
speed = 10

# Font
font = pygame.font.SysFont("Arial", 24)

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

    # New head
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

    snake.insert(0, new_head)

    # Eat food
    if new_head == food:
        score += 1
        food = random_food()

        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Rotate the snake based on its current direction
    if direction == (CELL_SIZE, 0):        # right
        current_snake_img = snake_img
    elif direction == (-CELL_SIZE, 0):     # left
        current_snake_img = pygame.transform.flip(snake_img, True, False)
    elif direction == (0, -CELL_SIZE):     # up
        current_snake_img = pygame.transform.rotate(snake_img, 90)
    elif direction == (0, CELL_SIZE):      # down
        current_snake_img = pygame.transform.rotate(snake_img, -90)

    # Draw snake
    for segment in snake:
        screen.blit(current_snake_img, segment)

    # Draw food
    screen.blit(food_img, food)

    # Draw score + level
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 120, 10))

    pygame.display.update()
    clock.tick(speed)
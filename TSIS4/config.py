# config.py
WIDTH, HEIGHT = 600, 480
CELL_SIZE = 20

COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

FPS = 60

# Colors
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
GRAY       = (80,  80,  80)
DARK_GRAY  = (40,  40,  40)
RED        = (220, 50,  50)
GREEN      = (80,  200, 80)
YELLOW     = (255, 220, 0)
ORANGE     = (255, 140, 0)
BLUE       = (60,  120, 255)
PURPLE     = (160, 60,  220)
DARK_RED   = (120, 0,   0)
CYAN       = (0,   220, 220)

# Food
FOOD_LIFETIME   = 6000   # ms — normal food disappears
POISON_LIFETIME = 8000   # ms

# Power-up
POWERUP_FIELD_LIFETIME = 8000   # ms on field
POWERUP_EFFECT_DURATION = 5000  # ms effect after collected

# Obstacles start at this level
OBSTACLE_START_LEVEL = 3
OBSTACLES_PER_LEVEL  = 4   # new blocks added each level

# Speed
BASE_SPEED        = 8    # cells/sec at level 1
SPEED_PER_LEVEL   = 1
SPEED_BOOST_MULT  = 1.6
SLOW_MOTION_MULT  = 0.5

# Score per food weight
FOOD_SCORE = {1: 1, 2: 3, 3: 5}
FOOD_PER_LEVEL = 5       # foods eaten to advance a level
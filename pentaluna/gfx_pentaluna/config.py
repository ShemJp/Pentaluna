# config.py

# Constants
WIDTH = 1024
HEIGHT = 768
ROWS = 6
COLUMNS = 8
start_x, start_y = 100, 355
offscreen_y = -450

party = None
dungeons = []
current_dungeon = None
current_enemy = None

# Colors
class color:
    RED = (196, 0, 0)
    BLUE = (0, 0, 196)
    YELLOW = (192, 128, 0)
    GREEN = (0, 128, 0)
    STEEL = (64, 128, 128)
    PINK = (192, 32, 128)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    PURPLE = (64, 0, 128)
    SHADOW = (32, 32, 64)
    HIGHLIGHT = (255, 255, 128)

    COLORS = [RED, BLUE, YELLOW, GREEN, STEEL, PINK]
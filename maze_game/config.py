"""Game-wide settings: window, world size, timing, text and difficulty levels."""

from dataclasses import dataclass

# ---------------------------------------------------------------- window ---
TITLE = "Finding the One Piece"
WIN_MESSAGE = "You have found the one piece"
LOSE_MESSAGE = "You failed. Better luck next time"

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 860
FPS = 10

# ----------------------------------------------------------------- world ---
TILE = 50                 # size of one maze cell in pixels
WORLD_SIZE = 1600         # the maze is WORLD_SIZE x WORLD_SIZE pixels
VIEWPORT_SIZE = 800       # how much of the maze is visible at once
VIEWPORT_POS = (50, 40)   # where the visible part is drawn on the screen
MAZE_BACKGROUND = (49, 113, 200)

# --------------------------------------------------------------- gameplay ---
START_LIVES = 3
TREASURE_POINTS = 10
ENEMY_KILL_POINTS = 10
CLOCK_BONUS_MS = 1000
ENEMY_STEP = 20           # pixels an enemy moves per frame
WAVE_SPEED = 40           # pixels a power wave moves per frame

# How many of each item a maze gets.
TREASURE_OFF_PATH = 20
TREASURE_ON_PATH = 20
CLOCKS_ON_PATH = 5
CLOCKS_OFF_PATH = 10
TRAP_WALLS = 40

# -------------------------------------------------------------------- audio ---
DEFAULT_MUSIC_VOLUME = 0.5
DEFAULT_SOUND_VOLUME = 1.0
VOLUME_STEP = 0.1


@dataclass(frozen=True)
class Level:
    """Difficulty settings for one level."""

    number: int
    path_spacing: int      # smaller -> more turns in the solution path
    wall_density: float    # chance that a free cell becomes a wall
    enemies: int
    starting_powers: int
    power_pickups: int
    time_limit_ms: int


LEVELS = {
    1: Level(1, path_spacing=160, wall_density=0.6, enemies=5,
             starting_powers=3, power_pickups=2, time_limit_ms=120_000),
    2: Level(2, path_spacing=120, wall_density=0.7, enemies=8,
             starting_powers=3, power_pickups=5, time_limit_ms=110_000),
    3: Level(3, path_spacing=80, wall_density=0.8, enemies=15,
             starting_powers=8, power_pickups=10, time_limit_ms=100_000),
}

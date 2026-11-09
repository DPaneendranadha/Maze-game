"""Random maze generation.

This module has no pygame dependency, so it can be unit-tested on its own.
Cells are identified by the pixel position of their top-left corner, e.g.
(0, 0), (50, 0), (100, 0), ... for a tile size of 50.

How a maze is built:
  1. Pick random "waypoints" with increasing x coordinates (`_pick_waypoints`).
  2. Join them with an L-shaped path, first along x then along y
     (`_walk_between`). This path is the guaranteed solution and is never
     walled off. Its last cell is the exit.
  3. Every other cell becomes a wall with probability `level.wall_density`.
  4. Treasure, clocks, power-ups, trap walls and enemies are scattered on top.
"""

import random
from collections import deque
from dataclasses import dataclass, field

from . import config
from .config import Level

Cell = tuple[int, int]


@dataclass
class MazeLayout:
    """Everything needed to build the sprites for one level."""

    solution: list[Cell]                 # path from (0, 0) to the exit
    exit: Cell
    walls: set[Cell] = field(default_factory=set)
    trap_walls: set[Cell] = field(default_factory=set)   # subset of `walls`
    treasure: set[Cell] = field(default_factory=set)
    clocks: set[Cell] = field(default_factory=set)
    power_pickups: set[Cell] = field(default_factory=set)
    enemies: list[Cell] = field(default_factory=list)


def generate_maze(level: Level,
                  size: int = config.WORLD_SIZE,
                  tile: int = config.TILE,
                  rng: random.Random | None = None) -> MazeLayout:
    rng = rng or random.Random()
    all_cells = [(x, y) for x in range(0, size, tile) for y in range(0, size, tile)]

    # 1-2. The guaranteed path from the top-left corner to the exit.
    waypoints = sorted(_pick_waypoints(0, size, level.path_spacing, tile, size, rng))
    solution = [(0, 0)]
    for target in waypoints:
        solution += _walk_between(solution[-1], target, tile)
    exit_cell = solution[-1]
    on_path = set(solution)

    # 3. Walls. The 3x3 area around the exit is always kept open.
    around_exit = {(exit_cell[0] + dx * tile, exit_cell[1] + dy * tile)
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    walls = {cell for cell in all_cells
             if cell not in on_path and cell not in around_exit
             and rng.random() < level.wall_density}
    off_path = [cell for cell in all_cells if cell not in walls and cell not in on_path]
    path_cells = sorted(on_path - {(0, 0), exit_cell})

    # 4. Items and enemies.
    layout = MazeLayout(solution=solution, exit=exit_cell, walls=walls)
    layout.treasure = (_sample(off_path, config.TREASURE_OFF_PATH, rng)
                       | _sample(path_cells, config.TREASURE_ON_PATH, rng))

    def without_items(cells):
        taken = layout.treasure | layout.clocks
        return [c for c in cells if c not in taken]

    layout.clocks = (_sample(without_items(path_cells), config.CLOCKS_ON_PATH, rng)
                     | _sample(without_items(off_path), config.CLOCKS_OFF_PATH, rng))
    layout.power_pickups = _sample(without_items(off_path), level.power_pickups, rng)
    layout.trap_walls = _sample(sorted(walls), config.TRAP_WALLS, rng)

    # Enemies start on the solution path, away from the player's corner.
    enemy_spots = [c for c in without_items(path_cells) if c[0] > 200 and c[1] > 200]
    enemy_spots = enemy_spots or path_cells
    layout.enemies = [rng.choice(enemy_spots) for _ in range(level.enemies)]
    return layout


def find_path(open_cells: set[Cell], start: Cell, end: Cell,
              tile: int = config.TILE) -> list[Cell] | None:
    """Shortest path between two cells using breadth-first search, or None."""
    previous: dict[Cell, Cell | None] = {start: None}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = previous[current]
            return path[::-1]
        x, y = current
        for neighbour in ((x + tile, y), (x - tile, y), (x, y + tile), (x, y - tile)):
            if neighbour in open_cells and neighbour not in previous:
                previous[neighbour] = current
                queue.append(neighbour)
    return None


def path_to_moves(path: list[Cell]) -> str:
    """Turn a path into a string of moves: R(ight), L(eft), U(p), D(own)."""
    moves = []
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        if x2 > x1:
            moves.append("R")
        elif x2 < x1:
            moves.append("L")
        elif y2 > y1:
            moves.append("D")
        else:
            moves.append("U")
    return "".join(moves)


def _pick_waypoints(start: int, end: int, spacing: int, tile: int, size: int,
                    rng: random.Random) -> list[Cell]:
    """Recursively split [start, end) at random x positions until the pieces
    are no wider than `spacing`; each split point gets a random y."""
    if end - start <= spacing:
        return []
    x = rng.randrange(start, end, tile)
    y = rng.randrange(0, size, tile)
    return ([(x, y)]
            + _pick_waypoints(start, x, spacing, tile, size, rng)
            + _pick_waypoints(x, end, spacing, tile, size, rng))


def _walk_between(start: Cell, end: Cell, tile: int) -> list[Cell]:
    """Cells visited moving right from `start` to `end`'s column, then up or
    down to its row. `start` itself is not included."""
    (x, y), (x_end, y_end) = start, end
    cells = []
    while x < x_end:
        x += tile
        cells.append((x, y))
    step = tile if y_end > y else -tile
    while y != y_end:
        y += step
        cells.append((x, y))
    return cells


def _sample(cells, count: int, rng: random.Random) -> set[Cell]:
    cells = list(cells)
    return set(rng.sample(cells, min(count, len(cells))))

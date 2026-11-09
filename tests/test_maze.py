import random

import pytest

from maze_game import config
from maze_game.maze import find_path, generate_maze, path_to_moves

SEEDS = range(25)


def all_cells():
    return {(x, y) for x in range(0, config.WORLD_SIZE, config.TILE)
            for y in range(0, config.WORLD_SIZE, config.TILE)}


@pytest.mark.parametrize("level_number", config.LEVELS)
@pytest.mark.parametrize("seed", SEEDS)
def test_exit_is_always_reachable(level_number, seed):
    layout = generate_maze(config.LEVELS[level_number], rng=random.Random(seed))
    open_cells = all_cells() - layout.walls
    assert find_path(open_cells, (0, 0), layout.exit) is not None


@pytest.mark.parametrize("level_number", config.LEVELS)
@pytest.mark.parametrize("seed", SEEDS)
def test_items_are_never_inside_walls(level_number, seed):
    layout = generate_maze(config.LEVELS[level_number], rng=random.Random(seed))
    items = layout.treasure | layout.clocks | layout.power_pickups | set(layout.enemies)
    assert not items & layout.walls
    assert layout.exit not in layout.walls
    assert (0, 0) not in layout.walls


@pytest.mark.parametrize("seed", SEEDS)
def test_items_do_not_overlap(seed):
    layout = generate_maze(config.LEVELS[1], rng=random.Random(seed))
    assert not layout.treasure & layout.clocks
    assert not layout.treasure & layout.power_pickups
    assert not layout.clocks & layout.power_pickups


@pytest.mark.parametrize("seed", SEEDS)
def test_layout_matches_level_settings(seed):
    level = config.LEVELS[3]
    layout = generate_maze(level, rng=random.Random(seed))
    assert len(layout.enemies) == level.enemies
    assert len(layout.power_pickups) == level.power_pickups
    assert layout.trap_walls <= layout.walls
    assert all(cell in all_cells() for cell in layout.solution)


def test_solution_path_is_connected():
    layout = generate_maze(config.LEVELS[2], rng=random.Random(1))
    for (x1, y1), (x2, y2) in zip(layout.solution, layout.solution[1:]):
        assert abs(x1 - x2) + abs(y1 - y2) == config.TILE


def test_same_seed_gives_same_maze():
    a = generate_maze(config.LEVELS[1], rng=random.Random(42))
    b = generate_maze(config.LEVELS[1], rng=random.Random(42))
    assert a == b


def test_find_path_returns_shortest_path():
    open_cells = {(0, 0), (50, 0), (100, 0), (100, 50), (0, 50), (0, 100), (50, 100), (100, 100)}
    path = find_path(open_cells, (0, 0), (100, 100))
    assert len(path) == 5
    assert path[0] == (0, 0) and path[-1] == (100, 100)


def test_find_path_returns_none_when_blocked():
    assert find_path({(0, 0), (100, 0)}, (0, 0), (100, 0)) is None


def test_path_to_moves():
    path = [(0, 0), (50, 0), (50, 50), (0, 50), (0, 0)]
    assert path_to_moves(path) == "RDLU"

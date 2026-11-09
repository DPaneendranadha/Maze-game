"""Sprites: static tiles, animated characters, enemies and power waves."""

import random

import pygame

from . import config
from .assets import load_image

# Directions, used to pick the rotated animation frames.
RIGHT, UP, LEFT, DOWN = 0, 1, 2, 3
DIRECTION_STEPS = {RIGHT: (1, 0), UP: (0, -1), LEFT: (-1, 0), DOWN: (0, 1)}


def in_world(rect: pygame.Rect) -> bool:
    limit = config.WORLD_SIZE - config.TILE
    return 0 <= rect.x <= limit and 0 <= rect.y <= limit


class Tile(pygame.sprite.Sprite):
    """A sprite with a single image that never moves (walls, treasure, exit)."""

    def __init__(self, x: int, y: int, image_name: str, size: int = config.TILE):
        super().__init__()
        self.image = load_image(image_name, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))


class Probe(pygame.sprite.Sprite):
    """An invisible sprite used to test what is at a position before moving there."""

    def __init__(self, x: int, y: int, size: int = config.TILE):
        super().__init__()
        self.rect = pygame.Rect(x, y, size, size)


class AnimatedSprite(pygame.sprite.Sprite):
    """A sprite that cycles through frames and can face four directions.

    The frames should face right; frames for the other directions are made by
    rotating/flipping them.
    """

    def __init__(self, x: int, y: int, frame_names: list[str], size: int = config.TILE):
        super().__init__()
        right = [load_image(name, (size, size)) for name in frame_names]
        self.frames = {
            RIGHT: right,
            UP: [pygame.transform.rotate(f, 90) for f in right],
            LEFT: [pygame.transform.flip(f, True, False) for f in right],
            DOWN: [pygame.transform.rotate(f, 270) for f in right],
        }
        self.direction = RIGHT
        self.frame_index = 0
        self.image = right[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def move_to(self, x: int, y: int, direction: int = RIGHT, animate: bool = True,
                hold_last_frame: bool = False) -> None:
        """Place the sprite at (x, y) facing `direction`.

        If `animate` is true, advance to the next frame (looping, unless
        `hold_last_frame` is set); otherwise show the first frame.
        """
        frames = self.frames[direction]
        if animate:
            self.frame_index += 1
            if self.frame_index >= len(frames):
                self.frame_index = len(frames) - 1 if hold_last_frame else 0
        else:
            self.frame_index = 0
        self.direction = direction
        self.image = frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def animate(self) -> None:
        """Advance the animation without moving."""
        self.move_to(self.rect.x, self.rect.y, self.direction)


class Enemy(AnimatedSprite):
    """Wanders randomly, never walking into walls or out of the maze."""

    def wander(self, blockers: pygame.sprite.Group,
               step: int = config.ENEMY_STEP, attempts: int = 20) -> None:
        for _ in range(attempts):
            direction = random.choice(list(DIRECTION_STEPS))
            dx, dy = DIRECTION_STEPS[direction]
            moved = self.rect.move(dx * step, dy * step)
            probe = Probe(moved.x, moved.y)
            if in_world(moved) and not pygame.sprite.spritecollideany(probe, blockers):
                self.move_to(moved.x, moved.y, direction)
                return


class Wave(AnimatedSprite):
    """A power attack that flies in a straight line until it hits something."""

    def __init__(self, x: int, y: int, frame_names: list[str], direction: int):
        super().__init__(x, y, frame_names)
        self.direction = direction

    def fly(self, speed: int = config.WAVE_SPEED) -> None:
        dx, dy = DIRECTION_STEPS[self.direction]
        self.move_to(self.rect.x + dx * speed, self.rect.y + dy * speed,
                     self.direction, hold_last_frame=True)
        if not in_world(self.rect):
            self.kill()

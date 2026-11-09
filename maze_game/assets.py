"""Loading images and sounds from the assets/ folder.

Images are cached, so loading the same picture many times (e.g. one per wall
tile) only reads the file from disk once.
"""

from functools import lru_cache
from pathlib import Path

import pygame

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"

# Animation frames, listed in the order they are played.
PLAYER_FRAMES = [f"player/player_{i}.png" for i in range(1, 8)]
ENEMY_FRAMES = [f"enemies/enemy_{i:02d}.png" for i in range(1, 11)]
CLOCK_FRAMES = [f"items/clock_{i}.png" for i in range(1, 6)]
POWER_FRAMES = [f"items/power_{i}.png" for i in range(1, 4)]
WAVE_FRAMES = [f"effects/wave_{i}.png" for i in range(1, 5)]


@lru_cache(maxsize=None)
def load_image(name: str, size: tuple[int, int] | None = None) -> pygame.Surface:
    """Load an image from assets/images, optionally scaled to `size`."""
    image = pygame.image.load(IMAGES_DIR / name).convert()
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image


class Sounds:
    """All sound effects plus the background music, with shared volume control."""

    EFFECTS = {
        "wall_bump": "wall_bump.mp3",
        "power": "power.mp3",
        "pickup": "pickup.mp3",
        "lose": "lose.mp3",
        "win": "win.mp3",
        "explosion": "explosion.wav",
        "click": "click.mp3",
    }

    def __init__(self, music_volume: float, sound_volume: float):
        self._effects = {
            name: pygame.mixer.Sound(SOUNDS_DIR / filename)
            for name, filename in self.EFFECTS.items()
        }
        pygame.mixer.music.load(SOUNDS_DIR / "background_music.mp3")
        self.music_volume = music_volume
        self.sound_volume = sound_volume
        self._apply_volumes()

    def play(self, name: str) -> None:
        self._effects[name].play()

    def start_music(self) -> None:
        pygame.mixer.music.play(loops=-1)

    def change_sound_volume(self, delta: float) -> None:
        self.sound_volume = _clamp_volume(self.sound_volume + delta)
        self._apply_volumes()

    def change_music_volume(self, delta: float) -> None:
        self.music_volume = _clamp_volume(self.music_volume + delta)
        self._apply_volumes()

    def _apply_volumes(self) -> None:
        pygame.mixer.music.set_volume(self.music_volume)
        for sound in self._effects.values():
            sound.set_volume(self.sound_volume)


def _clamp_volume(volume: float) -> float:
    return round(min(1.0, max(0.0, volume)), 1)

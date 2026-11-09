"""The game loop and its screens.

The game moves between five screens:

    TITLE -> LEVEL_SELECT -> PLAYING -> RESULTS -> GAME_OVER
                  ^                                   |
                  +------------ restart --------------+

Each screen has its own `_update_<screen>` method that handles input and
draws one frame.
"""

import sys
from enum import Enum, auto

import pygame

from . import config
from .assets import (CLOCK_FRAMES, ENEMY_FRAMES, PLAYER_FRAMES, POWER_FRAMES,
                     WAVE_FRAMES, Sounds, load_image)
from .config import TILE, Level
from .highscores import HighScores
from .maze import find_path, generate_maze
from .sprites import (DIRECTION_STEPS, DOWN, LEFT, RIGHT, UP, AnimatedSprite, Enemy,
                      Probe, Tile, Wave, in_world)

WHITE = (255, 255, 255)
GOLD = (255, 200, 40)
BLACK = (0, 0, 0)
SCREEN_RECT = pygame.Rect(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

ARROW_KEYS = {pygame.K_RIGHT: RIGHT, pygame.K_UP: UP,
              pygame.K_LEFT: LEFT, pygame.K_DOWN: DOWN}

def _button(width: int, height: int, center: tuple[int, int]) -> pygame.Rect:
    rect = pygame.Rect(0, 0, width, height)
    rect.center = center
    return rect


# Clickable areas. The buttons are part of the background pictures, so these
# rectangles just mark where they are drawn.
NEW_GAME_BUTTON = pygame.Rect(345, 700, 210, 50)
EXIT_BUTTON = pygame.Rect(570, 760, 120, 50)
LEVEL_BUTTONS = {
    1: _button(90, 90, (220, 615)),
    2: _button(90, 90, (340, 610)),
    3: _button(90, 90, (450, 610)),
}
LEVEL_KEYS = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3}
NEXT_BUTTON = pygame.Rect(700, 660, 200, 200)
RESTART_BUTTON = _button(200, 56, (450, 530))
HOME_BUTTON = _button(200, 56, (450, 600))
QUIT_BUTTON = _button(200, 56, (450, 680))


class Screen(Enum):
    TITLE = auto()
    LEVEL_SELECT = auto()
    PLAYING = auto()
    RESULTS = auto()
    GAME_OVER = auto()


# A glowing yellow dot drawn on each cell of the hint path.
HINT_MARKER = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
pygame.draw.circle(HINT_MARKER, (255, 220, 0, 90), (TILE // 2, TILE // 2), TILE // 2 - 4)
pygame.draw.circle(HINT_MARKER, (255, 240, 60, 255), (TILE // 2, TILE // 2), TILE // 6)


class Round:
    """The state of one attempt at a level: the maze, its sprites and the stats."""

    def __init__(self, level: Level):
        self.level = level
        self.layout = generate_maze(level)
        self.score = 0
        self.kills = 0
        self.lives = config.START_LIVES
        self.powers = level.starting_powers
        self.time_limit_ms = level.time_limit_ms
        self.start_ms = pygame.time.get_ticks()
        self.end_ms: int | None = None   # set when the round finishes; freezes the clock
        self.paused_at_ms: int | None = None
        self.paused_total_ms = 0
        self.won = False
        self.high_score_rank: int | None = None   # set when the round finishes
        self.previous_best: int | None = None
        self.hint_path: list[tuple[int, int]] = []
        self.hint_until_ms = 0
        self.open_cells = {(x, y) for x in range(0, config.WORLD_SIZE, TILE)
                           for y in range(0, config.WORLD_SIZE, TILE)} - self.layout.walls

        layout = self.layout
        self.player = AnimatedSprite(0, 0, PLAYER_FRAMES)
        self.walls = pygame.sprite.Group(
            Tile(x, y, "tiles/wall.jpg") for x, y in layout.walls - layout.trap_walls)
        self.trap_walls = pygame.sprite.Group(
            Tile(x, y, "tiles/trap_wall.jpg") for x, y in layout.trap_walls)
        self.treasure = pygame.sprite.Group(
            Tile(x, y, "items/treasure.png") for x, y in layout.treasure)
        self.clocks = pygame.sprite.Group(
            AnimatedSprite(x, y, CLOCK_FRAMES) for x, y in layout.clocks)
        self.power_pickups = pygame.sprite.Group(
            AnimatedSprite(x, y, POWER_FRAMES) for x, y in layout.power_pickups)
        self.enemies = pygame.sprite.Group(
            Enemy(x, y, ENEMY_FRAMES) for x, y in layout.enemies)
        self.exit = Tile(*layout.exit, "tiles/exit.jpg")
        self.waves = pygame.sprite.Group()

        # Things that hurt the player, and things enemies cannot walk through.
        self.hazards = pygame.sprite.Group(self.enemies, self.trap_walls)
        self.blockers = pygame.sprite.Group(self.walls, self.trap_walls)

    @property
    def remaining_ms(self) -> int:
        now = pygame.time.get_ticks()
        if self.end_ms is not None:
            now = self.end_ms
        elif self.paused_at_ms is not None:
            now = self.paused_at_ms
        return self.time_limit_ms - (now - self.start_ms - self.paused_total_ms)

    @property
    def paused(self) -> bool:
        return self.paused_at_ms is not None

    def toggle_pause(self) -> None:
        """Pause or resume. Time spent paused doesn't count against the clock."""
        now = pygame.time.get_ticks()
        if self.paused_at_ms is None:
            self.paused_at_ms = now
        else:
            paused_for = now - self.paused_at_ms
            self.paused_total_ms += paused_for
            self.hint_until_ms += paused_for   # a hint shown before pausing keeps its time
            self.paused_at_ms = None

    def finish(self, won: bool) -> None:
        """Stop the clock so the results screen shows the time at the finish."""
        self.end_ms = pygame.time.get_ticks()
        self.won = won

    def final_score(self) -> int:
        """Score plus bonuses for time and lives left."""
        return self.score + max(0, self.remaining_ms) // 100 + self.lives * 100

    def show_hint(self) -> None:
        """Work out the shortest way from the player to the exit and show it
        for a few seconds, in exchange for some time off the clock."""
        here = self.player.rect.topleft
        self.hint_path = find_path(self.open_cells, here, self.layout.exit) or []
        self.hint_until_ms = pygame.time.get_ticks() + config.HINT_DURATION_MS
        self.time_limit_ms -= config.HINT_COST_MS

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(config.MAZE_BACKGROUND)
        if pygame.time.get_ticks() < self.hint_until_ms:
            for cell in self.hint_path[1:-1]:
                surface.blit(HINT_MARKER, cell)
        for group in (self.walls, self.trap_walls, self.treasure, self.clocks,
                      self.power_pickups, self.enemies, self.waves):
            group.draw(surface)
        surface.blit(self.exit.image, self.exit.rect)
        surface.blit(self.player.image, self.player.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.maze_surface = pygame.Surface((config.WORLD_SIZE, config.WORLD_SIZE))
        self.camera = pygame.Rect(0, 0, config.VIEWPORT_SIZE, config.VIEWPORT_SIZE)

        self.hud_font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 80)
        self.title_font = pygame.font.Font(None, 70)
        self.level_font = pygame.font.Font(None, 100)

        self.sounds = Sounds(config.DEFAULT_MUSIC_VOLUME, config.DEFAULT_SOUND_VOLUME)
        self.sounds.start_music()

        self.high_scores = HighScores()
        self.state = Screen.TITLE
        self.round: Round | None = None
        self.running = True

    # ------------------------------------------------------------ main loop ---
    def run(self) -> None:
        handlers = {
            Screen.TITLE: self._update_title,
            Screen.LEVEL_SELECT: self._update_level_select,
            Screen.PLAYING: self._update_playing,
            Screen.RESULTS: self._update_results,
            Screen.GAME_OVER: self._update_game_over,
        }
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_volume_keys(event)
            handlers[self.state](events)
            pygame.display.flip()
            self.clock.tick(config.FPS)
        pygame.quit()

    def _handle_volume_keys(self, event: pygame.event.Event) -> None:
        """Shift + Up/Down changes sound effects, Tab + Up/Down changes music."""
        delta = {pygame.K_UP: config.VOLUME_STEP,
                 pygame.K_DOWN: -config.VOLUME_STEP}.get(event.key)
        if delta is None:
            return
        held = pygame.key.get_pressed()
        if held[pygame.K_LSHIFT]:
            self.sounds.change_sound_volume(delta)
        elif held[pygame.K_TAB]:
            self.sounds.change_music_volume(delta)

    def _draw_background(self, image_name: str) -> None:
        self.screen.blit(load_image(image_name, SCREEN_RECT.size), (0, 0))

    def _clicked(self, events, button: pygame.Rect) -> bool:
        return any(e.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(e.pos)
                   for e in events)

    # ---------------------------------------------------------------- screens ---
    def _update_title(self, events) -> None:
        self._draw_background("ui/title_screen.jpg")
        if self._clicked(events, NEW_GAME_BUTTON):
            self.sounds.play("click")
            self.state = Screen.LEVEL_SELECT
        elif self._clicked(events, EXIT_BUTTON) or _key_pressed(events, pygame.K_ESCAPE):
            self.sounds.play("click")
            self.running = False

    def _update_level_select(self, events) -> None:
        self._draw_background("ui/level_select.jpg")
        for number, button in LEVEL_BUTTONS.items():
            if self._clicked(events, button):
                self._start_level(number)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in LEVEL_KEYS:
                self._start_level(LEVEL_KEYS[event.key])
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = Screen.TITLE

    def _start_level(self, number: int) -> None:
        self.sounds.play("click")
        self.round = Round(config.LEVELS[number])
        self.state = Screen.PLAYING

    def _update_playing(self, events) -> None:
        game = self.round
        if _key_pressed(events, pygame.K_ESCAPE):   # give up and go home
            self.state = Screen.TITLE
            return
        if _key_pressed(events, pygame.K_p):
            game.toggle_pause()
        if game.paused:
            self._draw_play_area()
            self._draw_pause_overlay()
            return

        if _key_pressed(events, pygame.K_h):
            game.show_hint()
            self.sounds.play("power")

        held = pygame.key.get_pressed()
        if held[pygame.K_SPACE]:
            self._fire_waves(events)
        else:
            self._move_player(held)

        for wave in list(game.waves):
            wave.fly()
            self._resolve_wave_hits(wave)
        for enemy in game.enemies:
            enemy.wander(game.blockers)
        for item in (*game.clocks, *game.power_pickups):
            item.animate()

        self._draw_play_area()

        reached_exit = game.player.rect.colliderect(game.exit.rect)
        if reached_exit or game.lives <= 0 or game.remaining_ms <= 0:
            game.finish(won=reached_exit and game.lives > 0 and game.remaining_ms > 0)
            self._record_score()
            self.sounds.play("win" if game.won else "lose")
            self.state = Screen.RESULTS

    def _record_score(self) -> None:
        game = self.round
        game.previous_best = self.high_scores.best(game.level.number)
        game.high_score_rank = self.high_scores.add(game.level.number, game.final_score())

    def _move_player(self, held) -> None:
        game = self.round
        player = game.player
        direction = next((d for key, d in ARROW_KEYS.items() if held[key]), None)
        if direction is None:
            player.move_to(player.rect.x, player.rect.y, RIGHT, animate=False)
            return

        dx, dy = DIRECTION_STEPS[direction]
        target = Probe(player.rect.x + dx * TILE, player.rect.y + dy * TILE)
        if not in_world(target.rect):
            return

        if pygame.sprite.spritecollideany(target, game.hazards):
            self._lose_life()
        elif pygame.sprite.spritecollideany(target, game.walls):
            self.sounds.play("wall_bump")
        else:
            player.move_to(target.rect.x, target.rect.y, direction)
            self._collect_items()

    def _collect_items(self) -> None:
        game = self.round
        player = game.player
        if pygame.sprite.spritecollide(player, game.treasure, dokill=True):
            game.score += config.TREASURE_POINTS
            self.sounds.play("pickup")
        if pygame.sprite.spritecollide(player, game.clocks, dokill=True):
            game.time_limit_ms += config.CLOCK_BONUS_MS
            self.sounds.play("pickup")
        if pygame.sprite.spritecollide(player, game.power_pickups, dokill=True):
            game.powers += 1
            self.sounds.play("pickup")

    def _lose_life(self) -> None:
        """Show an explosion, pause for a second and send the player back to the start."""
        game = self.round
        game.lives -= 1
        self.sounds.play("explosion")
        self._flash_explosion("effects/explosion_player.png", game.player.rect)
        pygame.time.delay(1000)
        game.player.move_to(0, 0)

    def _fire_waves(self, events) -> None:
        """Space + an arrow key fires a power wave in that direction."""
        game = self.round
        for event in events:
            if event.type != pygame.KEYDOWN or event.key not in ARROW_KEYS:
                continue
            if game.powers <= 0:
                return
            game.powers -= 1
            self.sounds.play("power")
            game.waves.add(Wave(game.player.rect.x, game.player.rect.y,
                                WAVE_FRAMES, ARROW_KEYS[event.key]))

    def _resolve_wave_hits(self, wave: Wave) -> None:
        game = self.round
        for enemy in pygame.sprite.spritecollide(wave, game.enemies, dokill=False):
            wave.kill()
            enemy.kill()
            game.score += config.ENEMY_KILL_POINTS
            game.kills += 1
            self.sounds.play("explosion")
            self._flash_explosion("effects/explosion_enemy.png", enemy.rect)
        if pygame.sprite.spritecollideany(wave, game.walls):
            wave.kill()

    def _flash_explosion(self, image_name: str, where: pygame.Rect) -> None:
        self.maze_surface.blit(load_image(image_name, (TILE, TILE)), where)
        self.screen.blit(self.maze_surface, config.VIEWPORT_POS, self.camera)
        pygame.display.flip()

    def _draw_play_area(self) -> None:
        game = self.round
        # Keep the player in the middle of the view, but stop at the maze edges.
        max_offset = config.WORLD_SIZE - config.VIEWPORT_SIZE
        half = config.VIEWPORT_SIZE // 2
        self.camera.x = max(0, min(game.player.rect.x - half, max_offset))
        self.camera.y = max(0, min(game.player.rect.y - half, max_offset))

        self.screen.fill(BLACK)
        game.draw(self.maze_surface)
        self.screen.blit(self.maze_surface, config.VIEWPORT_POS, self.camera)

        seconds_left = max(0, game.remaining_ms) // 1000
        for text, x in ((f"Score: {game.score}", 10), (f"Power: {game.powers}", 200),
                        (f"Lives: {game.lives}", 500), (f"Time: {seconds_left}", 700)):
            self.screen.blit(self.hud_font.render(text, True, WHITE), (x, 10))

    def _draw_pause_overlay(self) -> None:
        shade = pygame.Surface(SCREEN_RECT.size, pygame.SRCALPHA)
        shade.fill((0, 0, 0, 150))
        self.screen.blit(shade, (0, 0))
        lines = [(self.level_font, "PAUSED", 380),
                 (self.hud_font, "P  resume      Esc  quit to title", 460)]
        for font, text, y in lines:
            rendered = font.render(text, True, WHITE)
            self.screen.blit(rendered, rendered.get_rect(center=(SCREEN_RECT.centerx, y)))

    def _update_results(self, events) -> None:
        game = self.round
        self._draw_background("ui/results.png")
        next_button = load_image("ui/next_button.jpg", NEXT_BUTTON.size).copy()
        next_button.set_alpha(150)
        self.screen.blit(next_button, NEXT_BUTTON)

        seconds_left = max(0, game.remaining_ms) // 1000 if game.won else 0
        message = config.WIN_MESSAGE if game.won else config.LOSE_MESSAGE
        texts = [
            (self.title_font, message, (450, 155)),
            (self.level_font, f"LEVEL-{game.level.number}", (450, 305)),
            (self.big_font, str(game.final_score()), (450, 420)),
            (self.big_font, str(game.lives), (852, 430)),
            (self.big_font, f"{seconds_left:02d}", (450, 655)),
            (self.big_font, f"Kills: {game.kills}", (125, 420)),
        ]
        if game.high_score_rank == 1:
            texts.append((self.title_font, "NEW HIGH SCORE!", (340, 790), GOLD))
        elif game.previous_best is not None:
            texts.append((self.title_font, f"Best: {game.previous_best}", (340, 790)))
        for font, text, center, *color in texts:
            rendered = font.render(text, True, color[0] if color else WHITE)
            self.screen.blit(rendered, rendered.get_rect(center=center))

        if self._clicked(events, NEXT_BUTTON):
            self.sounds.play("click")
            self.state = Screen.GAME_OVER

    def _update_game_over(self, events) -> None:
        self._draw_background("ui/game_over.png")
        if self._clicked(events, RESTART_BUTTON):
            self.sounds.play("click")
            self.state = Screen.LEVEL_SELECT
        elif self._clicked(events, HOME_BUTTON):
            self.sounds.play("click")
            self.state = Screen.TITLE
        elif self._clicked(events, QUIT_BUTTON):
            self.sounds.play("click")
            self.running = False


def _key_pressed(events, key: int) -> bool:
    return any(e.type == pygame.KEYDOWN and e.key == key for e in events)


def main() -> None:
    Game().run()
    sys.exit()

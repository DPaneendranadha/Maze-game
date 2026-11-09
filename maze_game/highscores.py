"""Best scores per level, saved to a small JSON file between runs.

The file lives in the user's data folder (see `default_path`) and looks like:

    {"1": [1497, 1210, 980], "2": [...], "3": [...]}

A missing or damaged file is treated as "no scores yet" rather than crashing
the game.
"""

import json
import os
import sys
from pathlib import Path

MAX_SCORES_PER_LEVEL = 5


def default_path() -> Path:
    """Where the high-score file is stored on this operating system."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / "maze-game" / "highscores.json"


class HighScores:
    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path else default_path()
        self._scores: dict[str, list[int]] = self._load()

    def top(self, level: int) -> list[int]:
        """Best scores for a level, highest first."""
        return list(self._scores.get(str(level), []))

    def best(self, level: int) -> int | None:
        scores = self.top(level)
        return scores[0] if scores else None

    def add(self, level: int, score: int) -> int | None:
        """Record a score. Returns its rank (1 = best) if it made the table,
        otherwise None. The table is saved immediately."""
        scores = self._scores.setdefault(str(level), [])
        # Ties go to the earlier score, so a new score ranks below equal ones.
        rank = 1 + sum(1 for s in scores if s >= score)
        if rank > MAX_SCORES_PER_LEVEL:
            return None
        scores.insert(rank - 1, score)
        del scores[MAX_SCORES_PER_LEVEL:]
        self._save()
        return rank

    def _load(self) -> dict[str, list[int]]:
        try:
            data = json.loads(self.path.read_text())
        except (OSError, ValueError):
            return {}
        if not isinstance(data, dict):
            return {}
        return {str(level): sorted((int(s) for s in scores if isinstance(s, (int, float))),
                                   reverse=True)[:MAX_SCORES_PER_LEVEL]
                for level, scores in data.items() if isinstance(scores, list)}

    def _save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self._scores, indent=2))
            tmp.replace(self.path)   # atomic, so a crash never leaves half a file
        except OSError:
            pass   # not being able to save scores should never stop the game

import json

from maze_game.highscores import MAX_SCORES_PER_LEVEL, HighScores


def test_empty_when_no_file(tmp_path):
    scores = HighScores(tmp_path / "scores.json")
    assert scores.top(1) == []
    assert scores.best(1) is None


def test_add_returns_rank_and_keeps_order(tmp_path):
    scores = HighScores(tmp_path / "scores.json")
    assert scores.add(1, 500) == 1
    assert scores.add(1, 900) == 1
    assert scores.add(1, 700) == 2
    assert scores.top(1) == [900, 700, 500]
    assert scores.best(1) == 900


def test_levels_are_separate(tmp_path):
    scores = HighScores(tmp_path / "scores.json")
    scores.add(1, 100)
    scores.add(2, 200)
    assert scores.top(1) == [100]
    assert scores.top(2) == [200]


def test_table_is_capped_and_low_scores_are_rejected(tmp_path):
    scores = HighScores(tmp_path / "scores.json")
    for value in range(100, 100 * (MAX_SCORES_PER_LEVEL + 1), 100):
        scores.add(1, value)
    assert len(scores.top(1)) == MAX_SCORES_PER_LEVEL
    assert scores.add(1, 50) is None
    assert 50 not in scores.top(1)


def test_tie_ranks_below_existing_score(tmp_path):
    scores = HighScores(tmp_path / "scores.json")
    scores.add(1, 500)
    assert scores.add(1, 500) == 2


def test_scores_persist_between_runs(tmp_path):
    path = tmp_path / "nested" / "scores.json"
    HighScores(path).add(3, 1234)
    assert HighScores(path).top(3) == [1234]
    assert json.loads(path.read_text()) == {"3": [1234]}


def test_damaged_file_is_ignored(tmp_path):
    path = tmp_path / "scores.json"
    path.write_text("{not json")
    scores = HighScores(path)
    assert scores.top(1) == []
    assert scores.add(1, 10) == 1


def test_unexpected_contents_are_cleaned(tmp_path):
    path = tmp_path / "scores.json"
    path.write_text(json.dumps({"1": [5, "oops", 9], "2": "nope"}))
    scores = HighScores(path)
    assert scores.top(1) == [9, 5]
    assert scores.top(2) == []

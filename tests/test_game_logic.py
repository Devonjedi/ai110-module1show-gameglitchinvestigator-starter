import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_winning_guess_message():
    outcome, message = check_guess(7, 7)
    assert "Correct" in message

def test_guess_too_high_outcome():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_high_hint_says_lower():
    # Hint must tell the player to go LOWER when guess is too high
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message.upper()

def test_guess_too_high_hint_does_not_say_higher():
    # Should NOT say HIGHER when guess is above the secret
    outcome, message = check_guess(60, 50)
    assert "HIGHER" not in message.upper()

def test_guess_too_low_outcome():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_guess_too_low_hint_says_higher():
    # Hint must tell the player to go HIGHER when guess is too low
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message.upper()

def test_guess_too_low_hint_does_not_say_lower():
    # Should NOT say LOWER when guess is below the secret
    outcome, message = check_guess(40, 50)
    assert "LOWER" not in message.upper()

def test_guess_at_boundary_low():
    # Guessing the lowest possible value that is still wrong
    outcome, message = check_guess(1, 2)
    assert outcome == "Too Low"

def test_guess_at_boundary_high():
    # Guessing one above the secret
    outcome, message = check_guess(100, 99)
    assert outcome == "Too High"

def test_check_guess_always_returns_two_values():
    result = check_guess(10, 20)
    assert len(result) == 2

def test_secret_is_always_compared_as_integer():
    # Passing secret as int should produce a win when guess matches
    outcome, _ = check_guess(42, 42)
    assert outcome == "Win"


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

def test_easy_range_smaller_than_normal():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high

def test_normal_range_smaller_than_hard():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert normal_high < hard_high

def test_easy_has_smallest_range():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high

def test_all_ranges_start_at_one():
    for difficulty in ["Easy", "Normal", "Hard"]:
        low, _ = get_range_for_difficulty(difficulty)
        assert low == 1, f"Expected low=1 for {difficulty}, got {low}"


# ---------------------------------------------------------------------------
# Attempt limits (defined as constants matching what app.py uses)
# ---------------------------------------------------------------------------

ATTEMPT_LIMIT_MAP = {
    "Easy": 10,
    "Normal": 7,
    "Hard": 5,
}

def test_easy_has_most_attempts():
    assert ATTEMPT_LIMIT_MAP["Easy"] > ATTEMPT_LIMIT_MAP["Normal"]

def test_normal_has_more_attempts_than_hard():
    assert ATTEMPT_LIMIT_MAP["Normal"] > ATTEMPT_LIMIT_MAP["Hard"]

def test_hard_has_fewest_attempts():
    assert ATTEMPT_LIMIT_MAP["Hard"] < ATTEMPT_LIMIT_MAP["Normal"] < ATTEMPT_LIMIT_MAP["Easy"]


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_float_truncates_to_int():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_empty_string_returns_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_none_returns_error():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_non_numeric_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_negative_number():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5

def test_parse_zero():
    ok, value, err = parse_guess("0")
    assert ok is True
    assert value == 0


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

def test_win_increases_score():
    new_score = update_score(0, "Win", 1)
    assert new_score > 0

def test_win_early_scores_more_than_win_late():
    early = update_score(0, "Win", 1)
    late = update_score(0, "Win", 8)
    assert early > late

def test_win_score_never_below_minimum():
    # Even on a very late attempt the score bonus should be at least 10
    score = update_score(0, "Win", 100)
    assert score >= 10

def test_too_low_decreases_score():
    new_score = update_score(100, "Too Low", 1)
    assert new_score < 100

def test_unknown_outcome_does_not_change_score():
    new_score = update_score(50, "Unknown", 1)
    assert new_score == 50

from logic_utils import check_guess, parse_guess, update_score


# --- check_guess ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- parse_guess ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False

def test_parse_word_is_invalid():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None

def test_parse_float_is_invalid():
    ok, value, err = parse_guess("3.5")
    assert ok is False


# --- update_score ---

def test_win_early_gives_high_score():
    score = update_score(0, "Win", 1)
    assert score > 50

def test_win_late_gives_minimum_points():
    score = update_score(0, "Win", 8)
    assert score == 10

def test_too_high_deducts_points():
    score = update_score(100, "Too High", 1)
    assert score == 95

def test_too_low_deducts_points():
    score = update_score(100, "Too Low", 1)
    assert score == 95

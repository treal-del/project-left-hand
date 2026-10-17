"""
test_logic.py - checks that the risk rules behave as intended.
Run with:  python test_logic.py   (or: pytest)
"""

from logic import (
    ACCESS_ARM, OTHER_ARM, UNSURE,
    EMERGENCY, HIGH, MODERATE, LOW,
    NSAID_REMINDER, assess,
)


def text(result):
    return " ".join(result.messages).lower()


def test_original_bug_access_warning_at_normal_bp():
    # Dialysis + arm pain at BP 120 used to get no access warning.
    r = assess(120, arm_pain=True, dialysis=True, pain_location=ACCESS_ARM)
    assert r.level == MODERATE
    assert "access site" in text(r)
    assert NSAID_REMINDER in r.messages


def test_arm_pain_alone_is_not_low():
    r = assess(130, arm_pain=True, dialysis=False)
    assert r.level == MODERATE


def test_chest_symptoms_are_an_emergency():
    r = assess(120, arm_pain=False, dialysis=False, chest_symptoms=True)
    assert r.level == EMERGENCY


def test_all_clear_is_low():
    r = assess(120, arm_pain=False, dialysis=False)
    assert r.level == LOW


def test_hypertensive_crisis_threshold():
    assert assess(180, False, False).level == MODERATE   # 180 is not above 180
    assert assess(181, False, False).level == EMERGENCY


def test_hypotension_threshold():
    assert assess(89, False, False).level == EMERGENCY
    assert assess(90, False, False).level == LOW


def test_hypotension_on_dialysis_mentions_staff():
    r = assess(85, False, True)
    assert r.level == EMERGENCY
    assert "dialysis nursing staff" in text(r)


def test_high_bp_with_dialysis_is_high():
    assert assess(150, False, True).level == HIGH


def test_high_bp_alone_is_moderate():
    assert assess(150, False, False).level == MODERATE


def test_pain_in_other_arm_on_dialysis_is_high_even_at_normal_bp():
    r = assess(120, True, True, pain_location=OTHER_ARM)
    assert r.level == HIGH
    assert "heart" in text(r)


def test_unsure_arm_gives_both_warnings():
    r = assess(120, True, True, pain_location=UNSURE)
    assert "access site" in text(r)
    assert "heart" in text(r)


def test_nsaid_reminder_only_for_dialysis():
    assert NSAID_REMINDER in assess(120, False, True).messages
    assert NSAID_REMINDER not in assess(120, False, False).messages


def test_invalid_bp_rejected():
    try:
        assess(0, False, False)
    except ValueError:
        return
    raise AssertionError("assess() should reject a BP of 0")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"\nAll {len(tests)} tests passed.")

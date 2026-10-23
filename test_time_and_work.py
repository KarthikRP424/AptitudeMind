import pytest
from answer_engine import verify_answer


def test_combined_work_returns_two_days():
    result = verify_answer({
        "topic": "Time and Work",
        "type": "COMBINED_WORK",
        "time_a": 6,
        "time_b": 3,
        "options": ["1", "2", "3", "4"],
    })

    assert result["status"] == "success"
    assert result["correct_answer"] == 2
    assert float(result["calculated_answer"]) == pytest.approx(2.0)


def test_zero_time_is_rejected():
    result = verify_answer({
        "topic": "Time and Work",
        "time_a": 0,
        "time_b": 3,
        "options": ["1", "2", "3", "4"],
    })

    assert result["status"] == "error"


def test_missing_time_is_rejected():
    result = verify_answer({
        "topic": "Time and Work",
        "time_b": 3,
        "options": ["1", "2", "3", "4"],
    })

    assert result["status"] == "error"


def test_unmatched_option_returns_error():
    result = verify_answer({
        "topic": "Time and Work",
        "time_a": 6,
        "time_b": 3,
        "options": ["5", "6", "7", "8"],
    })

    assert result["status"] == "error"
    assert "option" in result["message"].lower()

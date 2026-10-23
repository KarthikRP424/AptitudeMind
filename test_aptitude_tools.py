import pytest
import aptitude_tools as a


def test_empty_average_raises_value_error():
    with pytest.raises(ValueError, match="numbers cannot be empty"):
        a.calculate_average([])


def test_zero_time_raises_value_error():
    with pytest.raises(ValueError, match="time must be greater than zero"):
        a.calculate_speed(120, 0)


def test_zero_speed_raises_value_error():
    with pytest.raises(ValueError, match="speed must be greater than zero"):
        a.calculate_time(120, 0)


def test_invalid_percentage_input_raises_value_error():
    with pytest.raises(ValueError, match="valid number"):
        a.calculate_percentage("abc", 20)

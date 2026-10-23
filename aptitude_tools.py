
"""AptitudeMind - Aptitude Calculation Tools.

Provides calculation helpers for arithmetic and
Time-Speed-Distance aptitude questions.
"""


def _to_number(value, name):
    """Convert a value to a finite number or raise ValueError."""
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a number, not a boolean.")

    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a valid number.") from None

    if not __import__("math").isfinite(number):
        raise ValueError(f"{name} must be a finite number.")

    return number


def calculate_percentage(value, percentage):
    value = _to_number(value, "value")
    percentage = _to_number(percentage, "percentage")
    return value * percentage / 100


def calculate_profit(cost_price, profit_percentage):
    cost_price = _to_number(cost_price, "cost_price")
    profit_percentage = _to_number(
        profit_percentage, "profit_percentage"
    )

    if cost_price < 0:
        raise ValueError("cost_price cannot be negative.")

    if profit_percentage < 0:
        raise ValueError("profit_percentage cannot be negative.")

    profit = calculate_percentage(cost_price, profit_percentage)
    return cost_price + profit


def calculate_loss(cost_price, loss_percentage):
    cost_price = _to_number(cost_price, "cost_price")
    loss_percentage = _to_number(loss_percentage, "loss_percentage")

    if cost_price < 0:
        raise ValueError("cost_price cannot be negative.")

    if not 0 <= loss_percentage <= 100:
        raise ValueError("loss_percentage must be between 0 and 100.")

    loss = calculate_percentage(cost_price, loss_percentage)
    return cost_price - loss


def calculate_average(numbers):
    if numbers is None:
        raise ValueError("numbers cannot be None.")

    try:
        values = [_to_number(number, "list item") for number in numbers]
    except TypeError:
        raise ValueError("numbers must be an iterable of numbers.") from None

    if not values:
        raise ValueError("numbers cannot be empty.")

    return sum(values) / len(values)


def calculate_simple_interest(principal, rate, time):
    principal = _to_number(principal, "principal")
    rate = _to_number(rate, "rate")
    time = _to_number(time, "time")

    if principal < 0 or rate < 0 or time < 0:
        raise ValueError("principal, rate, and time cannot be negative.")

    return principal * rate * time / 100


def calculate_distance(speed, time):
    speed = _to_number(speed, "speed")
    time = _to_number(time, "time")

    if speed < 0 or time < 0:
        raise ValueError("speed and time cannot be negative.")

    return speed * time


def calculate_speed(distance, time):
    distance = _to_number(distance, "distance")
    time = _to_number(time, "time")

    if distance < 0 or time < 0:
        raise ValueError("distance and time cannot be negative.")

    if time == 0:
        raise ValueError("time must be greater than zero to calculate speed.")

    return distance / time


def calculate_time(distance, speed):
    distance = _to_number(distance, "distance")
    speed = _to_number(speed, "speed")

    if distance < 0 or speed < 0:
        raise ValueError("distance and speed cannot be negative.")

    if speed == 0:
        raise ValueError("speed must be greater than zero to calculate time.")

    return distance / speed

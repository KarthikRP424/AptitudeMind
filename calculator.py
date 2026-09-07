def calculate_percentage(value, percentage):
    return value * percentage / 100


def calculate_discount(value, percentage):
    discount = calculate_percentage(value, percentage)
    return value - discount


def calculate_increase(value, percentage):
    increase = calculate_percentage(value, percentage)
    return value + increase
def calculate_percentage(value, percentage):

    return value * percentage / 100


def calculate_profit(cost_price, profit_percentage):

    profit = calculate_percentage(
        cost_price,
        profit_percentage
    )

    return cost_price + profit


def calculate_loss(cost_price, loss_percentage):

    loss = calculate_percentage(
        cost_price,
        loss_percentage
    )

    return cost_price - loss


def calculate_average(numbers):

    return sum(numbers) / len(numbers)


def calculate_simple_interest(
    principal,
    rate,
    time
):

    return principal * rate * time / 100


def calculate_distance(
    speed,
    time
):

    return speed * time


def calculate_speed(
    distance,
    time
):

    return distance / time


def calculate_time(
    distance,
    speed
):

    return distance / speed
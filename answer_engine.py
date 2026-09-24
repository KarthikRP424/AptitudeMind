
"""
AptitudeMind - Answer Engine

Responsibilities:
1. Determine the correct answer for supported aptitude questions.
2. Use deterministic Python calculations instead of trusting the LLM.
3. Match the calculated answer against the four options.
4. Return the verified option number.
5. Provide an explanation.

Supported topics:
- Percentage
- Profit
- Profit Percentage
- Profit and Loss
- Loss
- Average
- Simple Interest
- Time-Speed-Distance
- Algebra
    - Linear Equation
    - Quadratic Equation
"""


from aptitude_tools import (
    calculate_percentage,
    calculate_profit,
    calculate_loss,
    calculate_average,
    calculate_simple_interest,
    calculate_distance,
    calculate_speed,
    calculate_time,
)


# ============================================================
# Utility Functions
# ============================================================

def approximately_equal(value1, value2, tolerance=1e-9):
    """
    Compare two numeric values safely.

    Floating-point calculations can sometimes produce tiny
    differences, so direct == comparison is avoided.
    """

    return abs(float(value1) - float(value2)) <= tolerance


def find_matching_option(calculated_answer, options):
    """
    Find which option matches the calculated answer.

    Returns:
        Option number (1-4), or None if no option matches.
    """

    if not isinstance(options, list):
        return None

    for index, option in enumerate(options, start=1):

        try:
            option_value = float(str(option).strip())

        except (ValueError, TypeError):
            continue

        if approximately_equal(
            calculated_answer,
            option_value
        ):
            return index

    return None


def create_result(
    status,
    topic,
    calculated_answer=None,
    correct_answer=None,
    explanation="",
    message=""
):
    """
    Create a consistent answer-engine result.
    """

    return {
        "status": status,
        "topic": topic,
        "calculated_answer": calculated_answer,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "message": message,
    }


# ============================================================
# Percentage
# ============================================================

def solve_percentage(question_data):
    """
    Calculate a percentage question.

    Expected internal data:

    {
        "value": 200,
        "percentage": 20,
        "options": ["20", "40", "60", "80"]
    }
    """

    value = question_data.get("value")
    percentage = question_data.get("percentage")
    options = question_data.get("options", [])

    if value is None or percentage is None:

        return create_result(
            status="error",
            topic="Percentage",
            message=(
                "Percentage question requires "
                "'value' and 'percentage'."
            )
        )

    answer = calculate_percentage(
        value,
        percentage
    )

    correct_option = find_matching_option(
        answer,
        options
    )

    if correct_option is None:

        return create_result(
            status="error",
            topic="Percentage",
            calculated_answer=answer,
            message=(
                "Calculated answer does not match "
                "any provided option."
            )
        )

    explanation = (
        f"{percentage}% of {value} = "
        f"{value} × {percentage} / 100 = {answer}"
    )

    return create_result(
        status="success",
        topic="Percentage",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message="Percentage answer verified successfully."
    )


# ============================================================
# Profit
# ============================================================

def solve_profit(question_data):
    """
    Calculate profit question.

    Expected internal data:

    {
        "cost_price": 1000,
        "profit_percentage": 20,
        "options": ["1100", "1200", "1300", "1400"]
    }
    """

    cost_price = question_data.get("cost_price")
    profit_percentage = question_data.get(
        "profit_percentage"
    )
    options = question_data.get("options", [])

    if cost_price is None or profit_percentage is None:

        return create_result(
            status="error",
            topic="Profit",
            message=(
                "Profit question requires "
                "'cost_price' and 'profit_percentage'."
            )
        )

    answer = calculate_profit(
        cost_price,
        profit_percentage
    )

    correct_option = find_matching_option(
        answer,
        options
    )

    if correct_option is None:

        return create_result(
            status="error",
            topic="Profit",
            calculated_answer=answer,
            message=(
                "Calculated answer does not match "
                "any provided option."
            )
        )

    profit = calculate_percentage(
        cost_price,
        profit_percentage
    )

    explanation = (
        f"Profit = {profit_percentage}% of {cost_price} "
        f"= {profit}. "
        f"Selling Price = {cost_price} + {profit} "
        f"= {answer}"
    )

    return create_result(
        status="success",
        topic="Profit",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message="Profit answer verified successfully."
    )


# ============================================================
# Profit Percentage
# ============================================================

def solve_profit_percentage(question_data):
    """
    Calculate profit percentage from cost price
    and selling price.

    Formula:

        Profit = Selling Price - Cost Price

        Profit Percentage =
            (Profit / Cost Price) × 100

    Expected internal data:

    {
        "cost_price": 500,
        "selling_price": 600,
        "options": ["10", "15", "20", "25"]
    }
    """

    cost_price = question_data.get(
        "cost_price"
    )

    selling_price = question_data.get(
        "selling_price"
    )

    options = question_data.get(
        "options",
        []
    )

    if cost_price is None or selling_price is None:

        return create_result(
            status="error",
            topic="Profit Percentage",
            message=(
                "Profit percentage question requires "
                "'cost_price' and 'selling_price'."
            )
        )

    try:

        cost_price = float(cost_price)
        selling_price = float(selling_price)

    except (TypeError, ValueError):

        return create_result(
            status="error",
            topic="Profit Percentage",
            message=(
                "Cost price and selling price "
                "must be numeric."
            )
        )

    if approximately_equal(
        cost_price,
        0
    ):

        return create_result(
            status="error",
            topic="Profit Percentage",
            message="Cost price cannot be zero."
        )

    profit = (
        selling_price - cost_price
    )

    answer = (
        profit / cost_price
    ) * 100

    correct_option = find_matching_option(
        answer,
        options
    )

    if correct_option is None:

        return create_result(
            status="error",
            topic="Profit Percentage",
            calculated_answer=answer,
            message=(
                "Calculated profit percentage does not "
                "match any provided option."
            )
        )

    explanation = (
        f"Profit = Selling Price - Cost Price\n"
        f"= {selling_price} - {cost_price}\n"
        f"= {profit}\n\n"
        f"Profit Percentage = "
        f"(Profit / Cost Price) × 100\n"
        f"= ({profit} / {cost_price}) × 100\n"
        f"= {answer}%"
    )

    return create_result(
        status="success",
        topic="Profit Percentage",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message=(
            "Profit percentage answer "
            "verified successfully."
        )
    )


# ============================================================
# Loss
# ============================================================

def solve_loss(question_data):
    """
    Calculate loss question.

    Expected internal data:

    {
        "cost_price": 1000,
        "loss_percentage": 20,
        "options": ["700", "800", "900", "1200"]
    }
    """

    cost_price = question_data.get("cost_price")
    loss_percentage = question_data.get(
        "loss_percentage"
    )
    options = question_data.get("options", [])

    if cost_price is None or loss_percentage is None:

        return create_result(
            status="error",
            topic="Loss",
            message=(
                "Loss question requires "
                "'cost_price' and 'loss_percentage'."
            )
        )

    answer = calculate_loss(
        cost_price,
        loss_percentage
    )

    correct_option = find_matching_option(
        answer,
        options
    )

    if correct_option is None:

        return create_result(
            status="error",
            topic="Loss",
            calculated_answer=answer,
            message=(
                "Calculated answer does not match "
                "any provided option."
            )
        )

    loss = calculate_percentage(
        cost_price,
        loss_percentage
    )

    explanation = (
        f"Loss = {loss_percentage}% of {cost_price} "
        f"= {loss}. "
        f"Selling Price = {cost_price} - {loss} "
        f"= {answer}"
    )

    return create_result(
        status="success",
        topic="Loss",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message="Loss answer verified successfully."
    )


# ============================================================
# Average
# ============================================================

def solve_average(question_data):
    """
    Calculate average question.

    Expected internal data:

    {
        "numbers": [10, 20, 30],
        "options": ["10", "20", "30", "40"]
    }
    """

    numbers = question_data.get("numbers")
    options = question_data.get("options", [])

    if not isinstance(numbers, list) or not numbers:

        return create_result(
            status="error",
            topic="Average",
            message=(
                "Average question requires "
                "a non-empty 'numbers' list."
            )
        )

    answer = calculate_average(numbers)

    correct_option = find_matching_option(
        answer,
        options
    )

    if correct_option is None:

        return create_result(
            status="error",
            topic="Average",
            calculated_answer=answer,
            message=(
                "Calculated answer does not match "
                "any provided option."
            )
        )

    total = sum(numbers)

    explanation = (
        f"Sum = {total}. "
        f"Number of values = {len(numbers)}. "
        f"Average = {total} / {len(numbers)} = {answer}"
    )

    return create_result(
        status="success",
        topic="Average",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message="Average answer verified successfully."
    )


# ============================================================
# Simple Interest
# ============================================================

def solve_simple_interest(question_data):
    """
    Calculate simple interest.

    Expected internal data:

    {
        "principal": 1000,
        "rate": 10,
        "time": 2,
        "options": ["100", "200", "300", "400"]
    }
    """

    principal = question_data.get("principal")
    rate = question_data.get("rate")
    time = question_data.get("time")
    options = question_data.get("options", [])

    if (
        principal is None
        or rate is None
        or time is None
    ):

        return create_result(
            status="error",
            topic="Simple Interest",
            message=(
                "Simple Interest question requires "
                "'principal', 'rate', and 'time'."
            )
        )

    answer = calculate_simple_interest(
        principal,
        rate,
        time
    )

    correct_option = find_matching_option(
        answer,
        options
    )

    if correct_option is None:

        return create_result(
            status="error",
            topic="Simple Interest",
            calculated_answer=answer,
            message=(
                "Calculated answer does not match "
                "any provided option."
            )
        )

    explanation = (
        f"SI = P × R × T / 100\n"
        f"= {principal} × {rate} × {time} / 100\n"
        f"= {answer}"
    )

    return create_result(
        status="success",
        topic="Simple Interest",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message="Simple Interest answer verified successfully."
    )


# ============================================================
# Distance
# ============================================================

def solve_distance(question_data):
    """
    Calculate distance.
    """

    speed = question_data.get("speed")
    time = question_data.get("time")
    options = question_data.get("options", [])

    if speed is None or time is None:

        return create_result(
            status="error",
            topic="Time-Speed-Distance",
            message=(
                "Distance question requires "
                "'speed' and 'time'."
            )
        )

    answer = calculate_distance(
        speed,
        time
    )

    correct_option = find_matching_option(
        answer,
        options
    )

    if correct_option is None:

        return create_result(
            status="error",
            topic="Time-Speed-Distance",
            calculated_answer=answer,
            message=(
                "Calculated answer does not match "
                "any provided option."
            )
        )

    explanation = (
        f"Distance = Speed × Time\n"
        f"= {speed} × {time}\n"
        f"= {answer}"
    )

    return create_result(
        status="success",
        topic="Time-Speed-Distance",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message="Distance answer verified successfully."
    )


# ============================================================
# Speed
# ============================================================

def solve_speed(question_data):
    """
    Calculate speed.
    """

    distance = question_data.get("distance")
    time = question_data.get("time")
    options = question_data.get("options", [])

    if distance is None or time is None:

        return create_result(
            status="error",
            topic="Time-Speed-Distance",
            message=(
                "Speed question requires "
                "'distance' and 'time'."
            )
        )

    if time == 0:

        return create_result(
            status="error",
            topic="Time-Speed-Distance",
            message="Time cannot be zero."
        )

    answer = calculate_speed(
        distance,
        time
    )

    correct_option = find_matching_option(
        answer,
        options
    )

    if correct_option is None:

        return create_result(
            status="error",
            topic="Time-Speed-Distance",
            calculated_answer=answer,
            message=(
                "Calculated answer does not match "
                "any provided option."
            )
        )

    explanation = (
        f"Speed = Distance / Time\n"
        f"= {distance} / {time}\n"
        f"= {answer}"
    )

    return create_result(
        status="success",
        topic="Time-Speed-Distance",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message="Speed answer verified successfully."
    )


# ============================================================
# Time
# ============================================================

def solve_time(question_data):
    """
    Calculate time.
    """

    distance = question_data.get("distance")
    speed = question_data.get("speed")
    options = question_data.get("options", [])

    if distance is None or speed is None:

        return create_result(
            status="error",
            topic="Time-Speed-Distance",
            message=(
                "Time question requires "
                "'distance' and 'speed'."
            )
        )

    if speed == 0:

        return create_result(
            status="error",
            topic="Time-Speed-Distance",
            message="Speed cannot be zero."
        )

    answer = calculate_time(
        distance,
        speed
    )

    correct_option = find_matching_option(
        answer,
        options
    )

    if correct_option is None:

        return create_result(
            status="error",
            topic="Time-Speed-Distance",
            calculated_answer=answer,
            message=(
                "Calculated answer does not match "
                "any provided option."
            )
        )

    explanation = (
        f"Time = Distance / Speed\n"
        f"= {distance} / {speed}\n"
        f"= {answer}"
    )

    return create_result(
        status="success",
        topic="Time-Speed-Distance",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message="Time answer verified successfully."
    )


# ============================================================
# Algebra - Numeric Option Parser
# ============================================================

def parse_numeric_option(option):
    """
    Convert common numeric option formats into a float.

    Supports:
        1
        -3
        0.5
        1/2
        -3/2
    """

    if isinstance(option, (int, float)):
        return float(option)

    if not isinstance(option, str):
        return None

    value = option.strip().replace("−", "-")

    try:
        return float(value)

    except ValueError:
        pass

    if "/" in value:

        parts = value.split("/")

        if len(parts) == 2:

            try:

                numerator = float(
                    parts[0].strip()
                )

                denominator = float(
                    parts[1].strip()
                )

                if denominator == 0:
                    return None

                return numerator / denominator

            except ValueError:

                return None

    return None


def find_matching_root_options(roots, options):
    """
    Find every option that matches any real root.

    Returns a list of option numbers.
    """

    if not isinstance(options, list):
        return []

    matching_options = []

    for index, option in enumerate(
        options,
        start=1
    ):

        option_value = parse_numeric_option(
            option
        )

        if option_value is None:
            continue

        for root in roots:

            if approximately_equal(
                root,
                option_value
            ):

                matching_options.append(index)
                break

    return matching_options


# ============================================================
# Algebra - Linear Equation
# ============================================================

def solve_linear_equation(question_data):
    """
    Solve a linear equation:

        ax + b = c
    """

    parameters = question_data.get(
        "parameters",
        {}
    )

    if not isinstance(parameters, dict):

        return create_result(
            status="error",
            topic="Algebra",
            message=(
                "Linear equation requires "
                "a 'parameters' dictionary."
            )
        )

    a = parameters.get("a")
    b = parameters.get("b")
    c = parameters.get("c")

    options = question_data.get(
        "options",
        []
    )

    if (
        a is None
        or b is None
        or c is None
    ):

        return create_result(
            status="error",
            topic="Algebra",
            message=(
                "Linear equation requires "
                "'a', 'b', and 'c'."
            )
        )

    try:

        a = float(a)
        b = float(b)
        c = float(c)

    except (TypeError, ValueError):

        return create_result(
            status="error",
            topic="Algebra",
            message=(
                "Linear equation coefficients "
                "must be numeric."
            )
        )

    if approximately_equal(a, 0):

        return create_result(
            status="error",
            topic="Algebra",
            message=(
                "Coefficient 'a' cannot be zero "
                "for a standard linear equation."
            )
        )

    answer = (c - b) / a

    correct_option = None

    for index, option in enumerate(
        options,
        start=1
    ):

        option_value = parse_numeric_option(
            option
        )

        if option_value is None:
            continue

        if approximately_equal(
            answer,
            option_value
        ):

            correct_option = index
            break

    if correct_option is None:

        return create_result(
            status="error",
            topic="Algebra",
            calculated_answer=answer,
            correct_answer=None,
            explanation=(
                f"x = (c - b) / a "
                f"= ({c} - {b}) / {a} "
                f"= {answer}. "
                "None of the provided options "
                "matches the calculated value."
            ),
            message=(
                "Linear equation answer does not "
                "match any provided option."
            )
        )

    explanation = (
        f"ax + b = c\n"
        f"x = (c - b) / a\n"
        f"x = ({c} - {b}) / {a}\n"
        f"x = {answer}"
    )

    return create_result(
        status="success",
        topic="Algebra",
        calculated_answer=answer,
        correct_answer=correct_option,
        explanation=explanation,
        message="Linear equation answer verified successfully."
    )


# ============================================================
# Algebra - Quadratic Equation
# ============================================================

def solve_quadratic_equation(question_data):
    """
    Solve a quadratic equation:

        ax² + bx + c = 0
    """

    parameters = question_data.get(
        "parameters",
        {}
    )

    if not isinstance(parameters, dict):

        return create_result(
            status="error",
            topic="Algebra",
            message=(
                "Quadratic equation requires "
                "a 'parameters' dictionary."
            )
        )

    a = parameters.get("a")
    b = parameters.get("b")
    c = parameters.get("c")

    options = question_data.get(
        "options",
        []
    )

    if (
        a is None
        or b is None
        or c is None
    ):

        return create_result(
            status="error",
            topic="Algebra",
            message=(
                "Quadratic equation requires "
                "'a', 'b', and 'c'."
            )
        )

    try:

        a = float(a)
        b = float(b)
        c = float(c)

    except (TypeError, ValueError):

        return create_result(
            status="error",
            topic="Algebra",
            message="Quadratic coefficients must be numeric."
        )

    if a == 0:

        return create_result(
            status="error",
            topic="Algebra",
            message=(
                "Coefficient 'a' cannot be zero "
                "for a quadratic equation."
            )
        )

    discriminant = (
        b ** 2
        - 4 * a * c
    )

    if discriminant < 0:

        explanation = (
            f"Discriminant = b² - 4ac = {discriminant}. "
            "Since the discriminant is negative, "
            "the equation has no real roots."
        )

        return create_result(
            status="success",
            topic="Algebra",
            calculated_answer="No real roots",
            correct_answer=None,
            explanation=explanation,
            message=(
                "Quadratic equation verified: "
                "no real roots."
            )
        )

    if approximately_equal(
        discriminant,
        0
    ):

        root = -b / (2 * a)

        roots = [root]

    else:

        sqrt_discriminant = (
            discriminant ** 0.5
        )

        root1 = (
            -b + sqrt_discriminant
        ) / (2 * a)

        root2 = (
            -b - sqrt_discriminant
        ) / (2 * a)

        roots = [
            root1,
            root2
        ]

    matching_options = find_matching_root_options(
        roots,
        options
    )

    if not matching_options:

        return create_result(
            status="error",
            topic="Algebra",
            calculated_answer=roots,
            correct_answer=None,
            explanation=(
                f"Discriminant = {discriminant}. "
                f"Real roots = {roots}. "
                "None of the provided options "
                "matches a calculated root."
            ),
            message=(
                "Quadratic answer does not match "
                "any provided option."
            )
        )

    if len(matching_options) == 1:

        correct_answer = matching_options[0]

    else:

        correct_answer = matching_options

    root_text = ", ".join(
        str(round(root, 10))
        for root in roots
    )

    explanation = (
        f"Discriminant = b² - 4ac = {discriminant}. "
        f"Roots = {root_text}. "
        f"Matching option(s) = {matching_options}."
    )

    return create_result(
        status="success",
        topic="Algebra",
        calculated_answer=roots,
        correct_answer=correct_answer,
        explanation=explanation,
        message=(
            "Quadratic equation answer verified successfully."
        )
    )


# ============================================================
# Main Answer Engine
# ============================================================

def verify_answer(question_data):
    """
    Select the correct deterministic solver based on topic.

    Returns a verified answer-engine result.
    """

    if not isinstance(question_data, dict):

        return create_result(
            status="error",
            topic=None,
            message="Question data must be a dictionary."
        )

    topic = question_data.get(
        "topic",
        ""
    )

    normalized_topic = topic.strip().lower()

    if normalized_topic == "percentage":

        return solve_percentage(
            question_data
        )

    if normalized_topic == "profit":

        return solve_profit(
            question_data
        )

    # --------------------------------------------------------
    # Profit Percentage
    #
    # Supports both:
    #     "Profit Percentage"
    #     "Profit and Loss"
    #
    # The Question Adapter currently produces:
    #
    #     topic = "Profit and Loss"
    #     type  = "PROFIT_PERCENTAGE"
    # --------------------------------------------------------

    if normalized_topic in {
        "profit percentage",
        "profit_percentage",
        "profit and loss",
    }:

        question_type = str(
            question_data.get(
                "type",
                ""
            )
        ).upper()

        # If the topic is specifically Profit and Loss,
        # make sure the question is actually a
        # profit-percentage question.
        if (
            normalized_topic == "profit and loss"
            and question_type != "PROFIT_PERCENTAGE"
        ):

            return create_result(
                status="error",
                topic=topic,
                message=(
                    "Profit and Loss question requires "
                    "'type': 'PROFIT_PERCENTAGE'."
                )
            )

        return solve_profit_percentage(
            question_data
        )

    if normalized_topic == "loss":

        return solve_loss(
            question_data
        )

    if normalized_topic == "average":

        return solve_average(
            question_data
        )

    if normalized_topic in {
        "simple interest",
        "simple_interest"
    }:

        return solve_simple_interest(
            question_data
        )

    if normalized_topic in {
        "time-speed-distance",
        "time speed distance",
        "speed",
        "distance",
        "time"
    }:

        question_type = question_data.get(
            "question_type"
        )

        if question_type == "distance":

            return solve_distance(
                question_data
            )

        if question_type == "speed":

            return solve_speed(
                question_data
            )

        if question_type == "time":

            return solve_time(
                question_data
            )

        return create_result(
            status="error",
            topic=topic,
            message=(
                "Time-Speed-Distance question requires "
                "'question_type': 'distance', 'speed', or 'time'."
            )
        )

    if normalized_topic in {
        "algebra",
        "quadratic",
        "quadratic equation",
    }:

        question_type = str(
            question_data.get(
                "type",
                ""
            )
        ).upper()

        if question_type == "LINEAR_EQUATION":

            return solve_linear_equation(
                question_data
            )

        if question_type == "QUADRATIC_EQUATION":

            return solve_quadratic_equation(
                question_data
            )

        return create_result(
            status="error",
            topic=topic,
            message=(
                "Algebra question requires "
                "'type': 'LINEAR_EQUATION' or "
                "'QUADRATIC_EQUATION'."
            )
        )

    return create_result(
        status="unsupported",
        topic=topic,
        message=(
            f"No deterministic answer solver exists "
            f"yet for topic '{topic}'."
        )
    )


# ============================================================
# Tests
# ============================================================

def run_tests():

    print(
        "\n🧪 AptitudeMind Answer Engine Tests"
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # Test 1 - Percentage
    # --------------------------------------------------------

    print("\nTest 1: Percentage")

    question = {
        "topic": "Percentage",
        "value": 200,
        "percentage": 20,
        "options": [
            "20",
            "40",
            "60",
            "80"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert result["calculated_answer"] == 40
    assert result["correct_answer"] == 2

    print("✅ Test 1 passed.")

    # --------------------------------------------------------
    # Test 2 - Profit
    # --------------------------------------------------------

    print("\nTest 2: Profit")

    question = {
        "topic": "Profit",
        "cost_price": 1000,
        "profit_percentage": 20,
        "options": [
            "1100",
            "1200",
            "1300",
            "1400"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert result["calculated_answer"] == 1200
    assert result["correct_answer"] == 2

    print("✅ Test 2 passed.")

    # --------------------------------------------------------
    # Test 3 - Loss
    # --------------------------------------------------------

    print("\nTest 3: Loss")

    question = {
        "topic": "Loss",
        "cost_price": 1000,
        "loss_percentage": 20,
        "options": [
            "700",
            "800",
            "900",
            "1200"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert result["calculated_answer"] == 800
    assert result["correct_answer"] == 2

    print("✅ Test 3 passed.")

    # --------------------------------------------------------
    # Test 4 - Average
    # --------------------------------------------------------

    print("\nTest 4: Average")

    question = {
        "topic": "Average",
        "numbers": [
            10,
            20,
            30
        ],
        "options": [
            "10",
            "20",
            "30",
            "40"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert result["calculated_answer"] == 20
    assert result["correct_answer"] == 2

    print("✅ Test 4 passed.")

    # --------------------------------------------------------
    # Test 5 - Simple Interest
    # --------------------------------------------------------

    print("\nTest 5: Simple Interest")

    question = {
        "topic": "Simple Interest",
        "principal": 1000,
        "rate": 10,
        "time": 2,
        "options": [
            "100",
            "200",
            "300",
            "400"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert result["calculated_answer"] == 200
    assert result["correct_answer"] == 2

    print("✅ Test 5 passed.")

    # --------------------------------------------------------
    # Test 6 - Distance
    # --------------------------------------------------------

    print("\nTest 6: Distance")

    question = {
        "topic": "Time-Speed-Distance",
        "question_type": "distance",
        "speed": 60,
        "time": 2,
        "options": [
            "60",
            "100",
            "120",
            "150"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert result["calculated_answer"] == 120
    assert result["correct_answer"] == 3

    print("✅ Test 6 passed.")

    # --------------------------------------------------------
    # Test 7 - Speed
    # --------------------------------------------------------

    print("\nTest 7: Speed")

    question = {
        "topic": "Time-Speed-Distance",
        "question_type": "speed",
        "distance": 120,
        "time": 2,
        "options": [
            "40",
            "60",
            "80",
            "100"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert result["calculated_answer"] == 60
    assert result["correct_answer"] == 2

    print("✅ Test 7 passed.")

    # --------------------------------------------------------
    # Test 8 - Time
    # --------------------------------------------------------

    print("\nTest 8: Time")

    question = {
        "topic": "Time-Speed-Distance",
        "question_type": "time",
        "distance": 120,
        "speed": 60,
        "options": [
            "1",
            "2",
            "3",
            "4"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert result["calculated_answer"] == 2
    assert result["correct_answer"] == 2

    print("✅ Test 8 passed.")

    # --------------------------------------------------------
    # Test 9 - Quadratic Equation
    # --------------------------------------------------------

    print("\nTest 9: Quadratic Equation")

    question = {
        "topic": "Algebra",
        "type": "QUADRATIC_EQUATION",
        "parameters": {
            "a": 2,
            "b": 5,
            "c": -3
        },
        "options": [
            "1/2",
            "-3/2",
            "-1",
            "3/2"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert result["correct_answer"] == 1
    assert approximately_equal(
        result["calculated_answer"][0],
        0.5
    )
    assert approximately_equal(
        result["calculated_answer"][1],
        -3
    )

    print("✅ Test 9 passed.")

    # --------------------------------------------------------
    # Test 10 - Quadratic Wrong Options
    # --------------------------------------------------------

    print("\nTest 10: Quadratic Wrong Options")

    question = {
        "topic": "Algebra",
        "type": "QUADRATIC_EQUATION",
        "parameters": {
            "a": 2,
            "b": 5,
            "c": -3
        },
        "options": [
            "1",
            "2",
            "3",
            "4"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "error"
    assert result["correct_answer"] is None

    print("✅ Test 10 passed.")

    # --------------------------------------------------------
    # Test 11 - Linear Equation
    # --------------------------------------------------------

    print("\nTest 11: Linear Equation")

    question = {
        "topic": "Algebra",
        "type": "LINEAR_EQUATION",
        "parameters": {
            "a": 2,
            "b": 5,
            "c": 11
        },
        "options": [
            "2",
            "3",
            "4",
            "5"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert approximately_equal(
        result["calculated_answer"],
        3
    )
    assert result["correct_answer"] == 2

    print("✅ Test 11 passed.")

    # --------------------------------------------------------
    # Test 12 - Linear Wrong Options
    # --------------------------------------------------------

    print("\nTest 12: Linear Wrong Options")

    question = {
        "topic": "Algebra",
        "type": "LINEAR_EQUATION",
        "parameters": {
            "a": 2,
            "b": 5,
            "c": 11
        },
        "options": [
            "1",
            "2",
            "4",
            "5"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "error"
    assert result["calculated_answer"] == 3
    assert result["correct_answer"] is None

    print("✅ Test 12 passed.")

    # --------------------------------------------------------
    # Test 13 - No matching Percentage option
    # --------------------------------------------------------

    print("\nTest 13: No matching Percentage option")

    question = {
        "topic": "Percentage",
        "value": 200,
        "percentage": 20,
        "options": [
            "10",
            "30",
            "50",
            "70"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "error"
    assert result["calculated_answer"] == 40
    assert result["correct_answer"] is None

    print("✅ Test 13 passed.")

    # --------------------------------------------------------
    # Test 14 - Profit Percentage
    # --------------------------------------------------------

    print("\nTest 14: Profit Percentage")

    question = {
        "topic": "Profit Percentage",
        "type": "PROFIT_PERCENTAGE",
        "cost_price": 500,
        "selling_price": 600,
        "options": [
            "10",
            "15",
            "20",
            "25"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "success"
    assert approximately_equal(
        result["calculated_answer"],
        20
    )
    assert result["correct_answer"] == 3

    print("✅ Test 14 passed.")

    # --------------------------------------------------------
    # Test 15 - Adapted Profit Percentage
    # --------------------------------------------------------

    print("\nTest 15: Adapted Profit Percentage")

    # This is the exact standardized format produced
    # by Question Adapter.

    question = {
        "question": (
            "An article is bought for ₹500 and sold for ₹600. "
            "What is the profit percentage?"
        ),
        "topic": "Profit and Loss",
        "type": "PROFIT_PERCENTAGE",
        "difficulty": "Easy",
        "company": "Infosys",
        "source": "company_style",
        "parameters": {
            "cost_price": 500,
            "selling_price": 600
        },
        "options": [
            "10",
            "15",
            "20",
            "25"
        ]
    }

    # The evaluator copies parameters to the top level
    # before calling the Answer Engine.
    prepared_question = dict(question)

    parameters = question.get(
        "parameters",
        {}
    )

    for key, value in parameters.items():

        prepared_question[key] = value

    result = verify_answer(
        prepared_question
    )

    print(result)

    assert result["status"] == "success"
    assert approximately_equal(
        result["calculated_answer"],
        20
    )
    assert result["correct_answer"] == 3

    print("✅ Test 15 passed.")

    print(
        "\n" + "=" * 60
    )

    print(
        "🎉 ALL ANSWER ENGINE TESTS PASSED"
    )

    print(
        "=" * 60
    )


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    run_tests()

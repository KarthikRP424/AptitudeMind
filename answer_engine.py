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
- Loss
- Average
- Simple Interest
- Time-Speed-Distance
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

    Expected internal data:

    {
        "speed": 60,
        "time": 2,
        "options": ["60", "100", "120", "150"]
    }
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

    Expected internal data:

    {
        "distance": 120,
        "time": 2,
        "options": ["40", "60", "80", "100"]
    }
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

    Expected internal data:

    {
        "distance": 120,
        "speed": 60,
        "options": ["1", "2", "3", "4"]
    }
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

    topic = question_data.get("topic", "")

    normalized_topic = topic.strip().lower()

    if normalized_topic == "percentage":

        return solve_percentage(question_data)

    if normalized_topic == "profit":

        return solve_profit(question_data)

    if normalized_topic == "loss":

        return solve_loss(question_data)

    if normalized_topic == "average":

        return solve_average(question_data)

    if normalized_topic in {
        "simple interest",
        "simple_interest"
    }:

        return solve_simple_interest(question_data)

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
            return solve_distance(question_data)

        if question_type == "speed":
            return solve_speed(question_data)

        if question_type == "time":
            return solve_time(question_data)

        return create_result(
            status="error",
            topic=topic,
            message=(
                "Time-Speed-Distance question requires "
                "'question_type': 'distance', 'speed', or 'time'."
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

    print("\n🧪 AptitudeMind Answer Engine Tests")
    print("=" * 60)

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
    # Test 9 - Unsupported topic
    # --------------------------------------------------------

    print("\nTest 9: Unsupported topic")

    question = {
        "topic": "Algebra",
        "options": [
            "1",
            "2",
            "3",
            "4"
        ]
    }

    result = verify_answer(question)

    print(result)

    assert result["status"] == "unsupported"

    print("✅ Test 9 passed.")

    # --------------------------------------------------------
    # Test 10 - Wrong options
    # --------------------------------------------------------

    print("\nTest 10: No matching option")

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

    print("✅ Test 10 passed.")

    print("\n" + "=" * 60)
    print("🎉 ALL ANSWER ENGINE TESTS PASSED")
    print("=" * 60)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    run_tests()
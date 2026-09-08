import json
import ollama

from aptitude_tools import (
    calculate_percentage,
    calculate_profit,
    calculate_loss,
    calculate_average,
    calculate_simple_interest,
    calculate_distance,
    calculate_speed,
    calculate_time
)

from progress import (
    record_result,
    show_progress,
    get_weak_topic
)

from topics import (
    get_available_topics,
    get_topic_types
)


MODEL = "llama3.2:3b"


# ============================================================
# PARSE AI RESPONSE
# ============================================================

def parse_response(result):

    try:
        # Remove markdown code fences if the model adds them
        result = result.strip()

        if result.startswith("```json"):
            result = result[7:]

        elif result.startswith("```"):
            result = result[3:]

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        data = json.loads(result)

        question = data.get("question", "")
        topic = data.get("topic", "")
        question_type = data.get("type", "").upper()
        parameters = data.get("parameters", {})

        return (
            question,
            topic,
            question_type,
            parameters
        )

    except json.JSONDecodeError:

        print("\n⚠️ AI returned invalid JSON.")
        print("Raw AI response:")
        print(result)

        return None, None, None, None


# ============================================================
# VALIDATE QUESTION
# ============================================================

def validate_question(
    question,
    topic,
    question_type,
    parameters
):

    # --------------------------------------------------------
    # Basic validation
    # --------------------------------------------------------

    if not question:
        return False, "Question is missing."

    if not topic:
        return False, "Topic is missing."

    if not question_type:
        return False, "Question type is missing."

    if not isinstance(parameters, dict):
        return False, "Parameters must be a JSON object."

    # --------------------------------------------------------
    # Topic validation
    # --------------------------------------------------------

    available_topics = get_available_topics()

    if topic not in available_topics:

        return False, (
            f"Unknown topic: {topic}"
        )

    # --------------------------------------------------------
    # Type validation
    # --------------------------------------------------------

    allowed_types = get_topic_types(topic)

    if question_type not in allowed_types:

        return False, (
            f"Invalid type '{question_type}' "
            f"for topic '{topic}'."
        )

    # ========================================================
    # PERCENTAGE
    # ========================================================

    if topic == "Percentage":

        if question_type == "PERCENTAGE":

            required = [
                "value",
                "percentage"
            ]

            for parameter in required:

                if parameter not in parameters:

                    return False, (
                        f"Missing parameter: {parameter}."
                    )

            try:

                value = float(
                    parameters["value"]
                )

                percentage = float(
                    parameters["percentage"]
                )

            except (ValueError, TypeError):

                return False, (
                    "Invalid percentage parameters."
                )

            if value <= 0:

                return False, (
                    "Value must be greater than zero."
                )

            if percentage <= 0:

                return False, (
                    "Percentage must be greater than zero."
                )

        elif question_type == "DISCOUNT":

            required = [
                "marked_price",
                "discount_percentage"
            ]

            for parameter in required:

                if parameter not in parameters:

                    return False, (
                        f"Missing parameter: {parameter}."
                    )

            try:

                marked_price = float(
                    parameters["marked_price"]
                )

                discount_percentage = float(
                    parameters["discount_percentage"]
                )

            except (ValueError, TypeError):

                return False, (
                    "Invalid discount parameters."
                )

            if marked_price <= 0:

                return False, (
                    "Marked price must be greater than zero."
                )

            if discount_percentage <= 0:

                return False, (
                    "Discount percentage must be greater than zero."
                )

            if discount_percentage >= 100:

                return False, (
                    "Discount percentage must be less than 100."
                )

        elif question_type == "INCREASE":

            required = [
                "original_value",
                "increase_percentage"
            ]

            for parameter in required:

                if parameter not in parameters:

                    return False, (
                        f"Missing parameter: {parameter}."
                    )

            try:

                original_value = float(
                    parameters["original_value"]
                )

                increase_percentage = float(
                    parameters["increase_percentage"]
                )

            except (ValueError, TypeError):

                return False, (
                    "Invalid increase parameters."
                )

            if original_value <= 0:

                return False, (
                    "Original value must be greater than zero."
                )

            if increase_percentage <= 0:

                return False, (
                    "Increase percentage must be greater than zero."
                )

    # ========================================================
    # PROFIT AND LOSS
    # ========================================================

    elif topic == "Profit and Loss":

        if "cost_price" not in parameters:

            return False, (
                "Missing parameter: cost_price."
            )

        try:

            cost_price = float(
                parameters["cost_price"]
            )

        except (ValueError, TypeError):

            return False, (
                "Invalid cost price."
            )

        if cost_price <= 0:

            return False, (
                "Cost price must be greater than zero."
            )

        if question_type == "PROFIT":

            if "profit_percentage" not in parameters:

                return False, (
                    "Missing parameter: profit_percentage."
                )

            try:

                profit_percentage = float(
                    parameters["profit_percentage"]
                )

            except (ValueError, TypeError):

                return False, (
                    "Invalid profit percentage."
                )

            if profit_percentage <= 0:

                return False, (
                    "Profit percentage must be greater than zero."
                )

        elif question_type == "LOSS":

            if "loss_percentage" not in parameters:

                return False, (
                    "Missing parameter: loss_percentage."
                )

            try:

                loss_percentage = float(
                    parameters["loss_percentage"]
                )

            except (ValueError, TypeError):

                return False, (
                    "Invalid loss percentage."
                )

            if loss_percentage <= 0:

                return False, (
                    "Loss percentage must be greater than zero."
                )

    # ========================================================
    # RATIO AND PROPORTION
    # ========================================================

    elif topic == "Ratio and Proportion":

        if "a" not in parameters:

            return False, "Missing parameter: a."

        if "b" not in parameters:

            return False, "Missing parameter: b."

        try:

            a = float(parameters["a"])
            b = float(parameters["b"])

        except (ValueError, TypeError):

            return False, "Invalid ratio values."

        if a <= 0 or b <= 0:

            return False, (
                "Ratio values must be greater than zero."
            )

    # ========================================================
    # AVERAGE
    # ========================================================

    elif topic == "Average":

        if "numbers" not in parameters:

            return False, (
                "Missing parameter: numbers."
            )

        numbers = parameters["numbers"]

        if not isinstance(numbers, list):

            return False, (
                "numbers must be a list."
            )

        if len(numbers) == 0:

            return False, (
                "Numbers list cannot be empty."
            )

        try:

            for number in numbers:

                float(number)

        except (ValueError, TypeError):

            return False, (
                "Invalid number in average list."
            )

    # ========================================================
    # SIMPLE INTEREST
    # ========================================================

    elif topic == "Simple Interest":

        required = [
            "principal",
            "rate",
            "time"
        ]

        for parameter in required:

            if parameter not in parameters:

                return False, (
                    f"Missing parameter: {parameter}."
                )

        try:

            principal = float(
                parameters["principal"]
            )

            rate = float(
                parameters["rate"]
            )

            time = float(
                parameters["time"]
            )

        except (ValueError, TypeError):

            return False, (
                "Invalid simple interest parameters."
            )

        if principal <= 0:
            return False, "Principal must be greater than zero."

        if rate <= 0:
            return False, "Rate must be greater than zero."

        if time <= 0:
            return False, "Time must be greater than zero."

    # ========================================================
    # TIME AND WORK
    # ========================================================

    elif topic == "Time and Work":

        if "days" not in parameters:

            return False, (
                "Missing parameter: days."
            )

        try:

            days = float(
                parameters["days"]
            )

        except (ValueError, TypeError):

            return False, (
                "Invalid days value."
            )

        if days <= 0:

            return False, (
                "Days must be greater than zero."
            )

    # ========================================================
    # TIME SPEED AND DISTANCE
    # ========================================================

    elif topic == "Time Speed and Distance":

        if question_type == "SPEED":

            required = [
                "distance",
                "time"
            ]

        elif question_type == "DISTANCE":

            required = [
                "speed",
                "time"
            ]

        elif question_type == "TIME":

            required = [
                "distance",
                "speed"
            ]

        else:

            return False, (
                "Unsupported speed/distance/time type."
            )

        for parameter in required:

            if parameter not in parameters:

                return False, (
                    f"Missing parameter: {parameter}."
                )

        try:

            for parameter in required:

                value = float(
                    parameters[parameter]
                )

                if value <= 0:

                    return False, (
                        f"{parameter} must be greater than zero."
                    )

        except (ValueError, TypeError):

            return False, (
                "Invalid speed/distance/time parameters."
            )

    # ========================================================
    # NUMBER SYSTEM
    # ========================================================

    elif topic == "Number System":

        if "number" not in parameters:

            return False, (
                "Missing parameter: number."
            )

        try:

            number = float(
                parameters["number"]
            )

        except (ValueError, TypeError):

            return False, (
                "Invalid number."
            )

    return True, "Valid"


# ============================================================
# GENERATE QUESTION
# ============================================================

def generate_question(topic_instruction):

    available_topics = get_available_topics()

    topic_text = "\n".join(
        f"- {topic}: {get_topic_types(topic)}"
        for topic in available_topics
    )

    prompt = f"""
You are AptitudeMind, an intelligent adaptive aptitude mentor.

{topic_instruction}

Available aptitude topics:

{topic_text}

Generate ONE aptitude question.

IMPORTANT RULES:

1. The question must be mathematically complete.
2. Every number required to solve the question must be provided.
3. Parameters must exactly match the question.
4. Never invent missing information.
5. Return ONLY valid JSON.
6. Do not use markdown.
7. Do not add explanations.
8. Generate only ONE question.

The JSON format MUST be:

{{
    "question": "question text",
    "topic": "topic name",
    "type": "QUESTION_TYPE",
    "parameters": {{
        "parameter_name": "value"
    }}
}}

============================================================
PERCENTAGE EXAMPLES
============================================================

Example:

{{
    "question": "What is 20% of 450?",
    "topic": "Percentage",
    "type": "PERCENTAGE",
    "parameters": {{
        "value": 450,
        "percentage": 20
    }}
}}

Discount example:

{{
    "question": "A discount of 15% is given on a marked price of ₹2400. What is the discounted price?",
    "topic": "Percentage",
    "type": "DISCOUNT",
    "parameters": {{
        "marked_price": 2400,
        "discount_percentage": 15
    }}
}}

Increase example:

{{
    "question": "A salary of ₹20000 is increased by 10%. What is the new salary?",
    "topic": "Percentage",
    "type": "INCREASE",
    "parameters": {{
        "original_value": 20000,
        "increase_percentage": 10
    }}
}}

============================================================
PROFIT AND LOSS EXAMPLES
============================================================

Profit:

{{
    "question": "A shopkeeper buys an item for ₹1000 and makes a profit of 20%. What is the selling price?",
    "topic": "Profit and Loss",
    "type": "PROFIT",
    "parameters": {{
        "cost_price": 1000,
        "profit_percentage": 20
    }}
}}

Loss:

{{
    "question": "A shopkeeper buys an item for ₹2000 and sells it at a loss of 10%. What is the selling price?",
    "topic": "Profit and Loss",
    "type": "LOSS",
    "parameters": {{
        "cost_price": 2000,
        "loss_percentage": 10
    }}
}}

============================================================
AVERAGE EXAMPLE
============================================================

{{
    "question": "Find the average of 10, 20, 30, 40 and 50.",
    "topic": "Average",
    "type": "AVERAGE",
    "parameters": {{
        "numbers": [10, 20, 30, 40, 50]
    }}
}}

============================================================
SIMPLE INTEREST EXAMPLE
============================================================

{{
    "question": "Find the simple interest on ₹5000 at 10% per year for 2 years.",
    "topic": "Simple Interest",
    "type": "SIMPLE_INTEREST",
    "parameters": {{
        "principal": 5000,
        "rate": 10,
        "time": 2
    }}
}}

============================================================
TIME SPEED DISTANCE EXAMPLE
============================================================

{{
    "question": "A car travels 120 km in 3 hours. What is its speed?",
    "topic": "Time Speed and Distance",
    "type": "SPEED",
    "parameters": {{
        "distance": 120,
        "time": 3
    }}
}}

============================================================

Do not generate an incomplete question.

Return ONLY JSON.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


# ============================================================
# CALCULATE ANSWER
# ============================================================

def calculate_answer(
    topic,
    question_type,
    parameters
):

    # ========================================================
    # PERCENTAGE
    # ========================================================

    if topic == "Percentage":

        if question_type == "PERCENTAGE":

            value = float(
                parameters["value"]
            )

            percentage = float(
                parameters["percentage"]
            )

            return calculate_percentage(
                value,
                percentage
            )

        elif question_type == "DISCOUNT":

            marked_price = float(
                parameters["marked_price"]
            )

            discount_percentage = float(
                parameters["discount_percentage"]
            )

            discount = calculate_percentage(
                marked_price,
                discount_percentage
            )

            return marked_price - discount

        elif question_type == "INCREASE":

            original_value = float(
                parameters["original_value"]
            )

            increase_percentage = float(
                parameters["increase_percentage"]
            )

            increase = calculate_percentage(
                original_value,
                increase_percentage
            )

            return original_value + increase

    # ========================================================
    # PROFIT AND LOSS
    # ========================================================

    elif topic == "Profit and Loss":

        cost_price = float(
            parameters["cost_price"]
        )

        if question_type == "PROFIT":

            profit_percentage = float(
                parameters["profit_percentage"]
            )

            return calculate_profit(
                cost_price,
                profit_percentage
            )

        elif question_type == "LOSS":

            loss_percentage = float(
                parameters["loss_percentage"]
            )

            return calculate_loss(
                cost_price,
                loss_percentage
            )

    # ========================================================
    # AVERAGE
    # ========================================================

    elif topic == "Average":

        numbers = [
            float(number)
            for number in parameters["numbers"]
        ]

        return calculate_average(numbers)

    # ========================================================
    # SIMPLE INTEREST
    # ========================================================

    elif topic == "Simple Interest":

        principal = float(
            parameters["principal"]
        )

        rate = float(
            parameters["rate"]
        )

        time = float(
            parameters["time"]
        )

        return calculate_simple_interest(
            principal,
            rate,
            time
        )

    # ========================================================
    # TIME SPEED DISTANCE
    # ========================================================

    elif topic == "Time Speed and Distance":

        if question_type == "SPEED":

            distance = float(
                parameters["distance"]
            )

            time = float(
                parameters["time"]
            )

            return calculate_speed(
                distance,
                time
            )

        elif question_type == "DISTANCE":

            speed = float(
                parameters["speed"]
            )

            time = float(
                parameters["time"]
            )

            return calculate_distance(
                speed,
                time
            )

        elif question_type == "TIME":

            distance = float(
                parameters["distance"]
            )

            speed = float(
                parameters["speed"]
            )

            return calculate_time(
                distance,
                speed
            )

    # ========================================================
    # RATIO
    # ========================================================

    elif topic == "Ratio and Proportion":

        a = float(
            parameters["a"]
        )

        b = float(
            parameters["b"]
        )

        return a / b

    # ========================================================
    # UNSUPPORTED
    # ========================================================

    return None


# ============================================================
# EXPLANATION
# ============================================================

def show_explanation(
    topic,
    question_type,
    parameters,
    correct_answer
):

    print("\n📖 Let's understand:")

    # ========================================================
    # PERCENTAGE
    # ========================================================

    if topic == "Percentage":

        if question_type == "PERCENTAGE":

            value = float(
                parameters["value"]
            )

            percentage = float(
                parameters["percentage"]
            )

            print(
                f"{percentage}% of {value}"
            )

            print(
                f"= {value} × {percentage} / 100"
            )

            print(
                f"= {correct_answer}"
            )

        elif question_type == "DISCOUNT":

            marked_price = float(
                parameters["marked_price"]
            )

            discount_percentage = float(
                parameters["discount_percentage"]
            )

            discount = calculate_percentage(
                marked_price,
                discount_percentage
            )

            print(
                f"Discount = {discount_percentage}% of ₹{marked_price}"
            )

            print(
                f"= ₹{marked_price} × {discount_percentage} / 100"
            )

            print(
                f"= ₹{discount}"
            )

            print("\nDiscounted price:")

            print(
                f"= ₹{marked_price} - ₹{discount}"
            )

            print(
                f"= ₹{correct_answer}"
            )

        elif question_type == "INCREASE":

            original_value = float(
                parameters["original_value"]
            )

            increase_percentage = float(
                parameters["increase_percentage"]
            )

            increase = calculate_percentage(
                original_value,
                increase_percentage
            )

            print(
                f"Increase = {increase_percentage}% of ₹{original_value}"
            )

            print(
                f"= ₹{increase}"
            )

            print("\nNew value:")

            print(
                f"= ₹{original_value} + ₹{increase}"
            )

            print(
                f"= ₹{correct_answer}"
            )

    # ========================================================
    # PROFIT AND LOSS
    # ========================================================

    elif topic == "Profit and Loss":

        cost_price = float(
            parameters["cost_price"]
        )

        if question_type == "PROFIT":

            profit_percentage = float(
                parameters["profit_percentage"]
            )

            profit = calculate_percentage(
                cost_price,
                profit_percentage
            )

            print(
                f"Profit = {profit_percentage}% of ₹{cost_price}"
            )

            print(
                f"= ₹{profit}"
            )

            print("\nSelling price:")

            print(
                f"= ₹{cost_price} + ₹{profit}"
            )

            print(
                f"= ₹{correct_answer}"
            )

        elif question_type == "LOSS":

            loss_percentage = float(
                parameters["loss_percentage"]
            )

            loss = calculate_percentage(
                cost_price,
                loss_percentage
            )

            print(
                f"Loss = {loss_percentage}% of ₹{cost_price}"
            )

            print(
                f"= ₹{loss}"
            )

            print("\nSelling price:")

            print(
                f"= ₹{cost_price} - ₹{loss}"
            )

            print(
                f"= ₹{correct_answer}"
            )

    # ========================================================
    # AVERAGE
    # ========================================================

    elif topic == "Average":

        numbers = parameters["numbers"]

        total = sum(
            float(number)
            for number in numbers
        )

        count = len(numbers)

        print(
            f"Sum = {total}"
        )

        print(
            f"Number of values = {count}"
        )

        print(
            f"Average = {total} / {count}"
        )

        print(
            f"= {correct_answer}"
        )

    # ========================================================
    # SIMPLE INTEREST
    # ========================================================

    elif topic == "Simple Interest":

        principal = float(
            parameters["principal"]
        )

        rate = float(
            parameters["rate"]
        )

        time = float(
            parameters["time"]
        )

        print(
            "SI = P × R × T / 100"
        )

        print(
            f"= {principal} × {rate} × {time} / 100"
        )

        print(
            f"= {correct_answer}"
        )

    # ========================================================
    # TIME SPEED DISTANCE
    # ========================================================

    elif topic == "Time Speed and Distance":

        if question_type == "SPEED":

            distance = float(
                parameters["distance"]
            )

            time = float(
                parameters["time"]
            )

            print(
                "Speed = Distance / Time"
            )

            print(
                f"= {distance} / {time}"
            )

            print(
                f"= {correct_answer}"
            )

        elif question_type == "DISTANCE":

            speed = float(
                parameters["speed"]
            )

            time = float(
                parameters["time"]
            )

            print(
                "Distance = Speed × Time"
            )

            print(
                f"= {speed} × {time}"
            )

            print(
                f"= {correct_answer}"
            )

        elif question_type == "TIME":

            distance = float(
                parameters["distance"]
            )

            speed = float(
                parameters["speed"]
            )

            print(
                "Time = Distance / Speed"
            )

            print(
                f"= {distance} / {speed}"
            )

            print(
                f"= {correct_answer}"
            )


# ============================================================
# MAIN AGENT
# ============================================================

def main():

    print("🤖 AptitudeMind is starting...\n")

    # --------------------------------------------------------
    # Get weak topic from memory
    # --------------------------------------------------------

    weak_topic = get_weak_topic()

    available_topics = get_available_topics()

    # --------------------------------------------------------
    # Adaptive topic selection
    # --------------------------------------------------------

    if weak_topic:

        print(
            f"🎯 Current focus topic: {weak_topic}"
        )

        topic_instruction = f"""
The student's current weakest topic is:

{weak_topic}

Generate the question from this topic.

Choose an appropriate question type from the
allowed types for that topic.
"""

    else:

        print(
            "🎯 No weak topic detected."
        )

        topic_instruction = f"""
Choose ONE topic from these available topics:

{available_topics}

Choose a suitable beginner-level topic.
"""

    # --------------------------------------------------------
    # Generate question
    # --------------------------------------------------------

    result = generate_question(
        topic_instruction
    )

    # --------------------------------------------------------
    # Parse AI response
    # --------------------------------------------------------

    (
        question,
        topic,
        question_type,
        parameters
    ) = parse_response(result)

    if question is None:

        print(
            "\n🔄 Question rejected."
        )

        return

    # --------------------------------------------------------
    # Debug information
    # --------------------------------------------------------

    print("\n🔍 AI Generated Data:")

    print(
        "Question:",
        question
    )

    print(
        "Topic:",
        topic
    )

    print(
        "Type:",
        question_type
    )

    print(
        "Parameters:",
        parameters
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    valid, message = validate_question(
        question,
        topic,
        question_type,
        parameters
    )

    if not valid:

        print(
            "\n⚠️ Invalid question generated."
        )

        print(
            "Reason:",
            message
        )

        print(
            "\n🔄 Question rejected."
        )

        return

    # --------------------------------------------------------
    # Calculate answer
    # --------------------------------------------------------

    try:

        correct_answer = calculate_answer(
            topic,
            question_type,
            parameters
        )

    except Exception as error:

        print(
            "\n⚠️ Calculator error:"
        )

        print(error)

        return

    if correct_answer is None:

        print(
            "\n⚠️ Verification tool is not ready."
        )

        print(
            "Topic:",
            topic
        )

        print(
            "Type:",
            question_type
        )

        return

    # --------------------------------------------------------
    # Show question to student
    # --------------------------------------------------------

    print("\n🧠 AptitudeMind:")

    print(
        "\n📚 Question:",
        question
    )

    student_answer = input(
        "\n👨‍🎓 Your answer: "
    )

    # --------------------------------------------------------
    # Evaluate student answer
    # --------------------------------------------------------

    try:

        student_value = float(
            student_answer
        )

        if abs(
            student_value - correct_answer
        ) < 0.01:

            print(
                "\n✅ Correct! Excellent work! 🔥"
            )

            print(
                "🧠 You calculated the answer correctly."
            )

            record_result(
                topic,
                True
            )

        else:

            print(
                "\n❌ Incorrect."
            )

            print(
                "💡 Correct answer:",
                correct_answer
            )

            record_result(
                topic,
                False
            )

            show_explanation(
                topic,
                question_type,
                parameters,
                correct_answer
            )

    except ValueError:

        print(
            "\n⚠️ Please enter a valid numerical answer."
        )

        record_result(
            topic,
            False
        )

    # --------------------------------------------------------
    # Show progress
    # --------------------------------------------------------

    show_progress()

    # --------------------------------------------------------
    # Show current weak topic
    # --------------------------------------------------------

    weak_topic = get_weak_topic()

    if weak_topic:

        print(
            f"\n🎯 AptitudeMind focus: {weak_topic}"
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    main()
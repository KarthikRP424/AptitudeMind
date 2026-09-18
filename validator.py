import re


def validate_question(question_data):
    """
    Validate the structure, wording, and basic mathematical consistency
    of an AptitudeMind question.
    """

    errors = []

    if not isinstance(question_data, dict):
        return {
            "valid": False,
            "errors": ["Question data must be a dictionary."]
        }

    question = question_data.get("question", "").strip()

    if not question:
        errors.append("Question text is missing.")

    topic = question_data.get("topic")

    if not topic:
        errors.append("Topic is missing.")

    difficulty = question_data.get("difficulty")

    if difficulty not in ["Easy", "Medium", "Hard"]:
        errors.append("Invalid or missing difficulty.")

    company = question_data.get("company")

    if not company:
        errors.append("Company information is missing.")

    options = question_data.get("options")

    if options is not None:

        if not isinstance(options, list):
            errors.append("Options must be a list.")

        elif len(options) < 2:
            errors.append("Question should contain at least two options.")

    if question and len(question) < 10:
        errors.append("Question text is too short.")

    # -----------------------------------------
    # AMBIGUOUS WORDING CHECK
    # -----------------------------------------

    ambiguous_phrases = [
        "one of the roots",
        "one of the answers",
        "any value",
        "could be",
        "might be"
    ]

    for phrase in ambiguous_phrases:

        if phrase in question.lower():

            errors.append(
                f"Potentially ambiguous wording: '{phrase}'."
            )

    # -----------------------------------------
    # TOPIC-SPECIFIC VALIDATION
    # -----------------------------------------

    if topic == "Algebra":
        errors.extend(
            validate_algebra_question(question)
        )

    if topic == "Percentage":
        errors.extend(
            validate_percentage_question(question)
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_algebra_question(question):
    """
    Validate Algebra questions for basic mathematical consistency.
    """

    errors = []

    q = question.lower()

    # -----------------------------------------
    # QUADRATIC EQUATION CHECK
    # -----------------------------------------

    if "quadratic equation" in q and "=" in question:

        root_keywords = [
            "roots",
            "root",
            "sum of the roots",
            "product of the roots",
            "discriminant"
        ]

        if not any(keyword in q for keyword in root_keywords):

            errors.append(
                "Quadratic equation lacks clear root context."
            )

    # -----------------------------------------
    # AMBIGUOUS ROOT QUESTION
    # -----------------------------------------

    if "what is the value of one of the roots" in q:

        errors.append(
            "Question asks for 'one of the roots' "
            "without uniquely identifying a root."
        )

    # -----------------------------------------
    # ROOT RATIO CHECK
    # -----------------------------------------

    if "sum and product of the roots" in q and "ratio" in q:

        errors.append(
            "Root ratio question requires mathematical "
            "verification before being accepted."
        )

    # -----------------------------------------
    # QUADRATIC COEFFICIENT CHECK
    # -----------------------------------------

    quadratic_match = re.search(
        r"([+-]?\d*\.?\d*)\s*x\^2\s*"
        r"([+-]\s*\d*\.?\d*)\s*x\s*"
        r"([+-]\s*\d*\.?\d*)\s*=\s*0",
        question,
        re.IGNORECASE
    )

    if quadratic_match:

        a_text = quadratic_match.group(1)
        b_text = quadratic_match.group(2)
        c_text = quadratic_match.group(3)

        a = parse_coefficient(a_text, default=1)
        b = parse_coefficient(b_text, default=0)
        c = parse_coefficient(c_text, default=0)

        # Sum of roots = -b/a
        expected_sum = -b / a

        # -----------------------------------------
        # DETECT CLAIMED SUM OF ROOTS
        # -----------------------------------------

        sum_match = re.search(
            r"sum of (?:the )?roots(?:.*?is|.*?=)\s*"
            r"(-?\d+(?:\.\d+)?)",
            q
        )

        if sum_match:

            claimed_sum = float(sum_match.group(1))

            if abs(expected_sum - claimed_sum) > 0.000001:

                errors.append(
                    f"Mathematical inconsistency: "
                    f"sum of roots should be {format_number(expected_sum)}, "
                    f"not {format_number(claimed_sum)}."
                )

        # -----------------------------------------
        # DETECT CLAIMED PRODUCT OF ROOTS
        # -----------------------------------------

        product_match = re.search(
            r"product of (?:the )?roots(?:.*?is|.*?=)\s*"
            r"(-?\d+(?:\.\d+)?)",
            q
        )

        if product_match:

            claimed_product = float(
                product_match.group(1)
            )

            expected_product = c / a

            if abs(expected_product - claimed_product) > 0.000001:

                errors.append(
                    f"Mathematical inconsistency: "
                    f"product of roots should be "
                    f"{format_number(expected_product)}, "
                    f"not {format_number(claimed_product)}."
                )

    return errors


def parse_coefficient(value, default=0):
    """
    Convert a coefficient string into a number.
    """

    value = value.strip().replace(" ", "")

    if value in ["", "+"]:
        return default if value == "" else 1

    if value == "-":
        return -1

    return float(value)


def format_number(value):
    """
    Display integers without unnecessary decimal places.
    """

    if value == int(value):
        return str(int(value))

    return str(round(value, 4))


def validate_percentage_question(question):
    """
    Validate basic Percentage question structure.
    """

    errors = []

    q = question.lower()

    if not any(
        word in q
        for word in ["%", "percent", "percentage"]
    ):

        errors.append(
            "Percentage topic question has no percentage context."
        )

    discount_words = [
        "discount",
        "discounted",
        "marked price",
        "selling price"
    ]

    if any(word in q for word in discount_words):

        if "price" not in q:

            errors.append(
                "Discount question does not clearly identify a price."
            )

    return errors


def show_validation(result):
    """
    Display validation result.
    """

    print("\n🛡️ Question Validation")
    print("----------------------")

    if result["valid"]:

        print("Status: ✅ VALID")

    else:

        print("Status: ❌ INVALID")

        print("\n⚠️ Errors:")

        for error in result["errors"]:
            print("-", error)


if __name__ == "__main__":

    print("🧠 AptitudeMind Validator")

    # -----------------------------------------
    # TEST 1: VALID QUESTION
    # -----------------------------------------

    valid_question = {
        "question": "What is 25% of 200?",
        "topic": "Percentage",
        "difficulty": "Easy",
        "company": "TCS",
        "options": ["40", "50", "60", "70"]
    }

    print("\nTest 1: Valid Percentage Question")

    result = validate_question(valid_question)

    show_validation(result)

    # -----------------------------------------
    # TEST 2: INVALID STRUCTURE
    # -----------------------------------------

    invalid_question = {
        "question": "",
        "topic": "Percentage",
        "difficulty": "Unknown",
        "company": "",
        "options": ["100"]
    }

    print("\nTest 2: Invalid Question")

    result = validate_question(invalid_question)

    show_validation(result)

    # -----------------------------------------
    # TEST 3: BAD ALGEBRA QUESTION
    # -----------------------------------------

    bad_algebra_question = {
        "question": (
            "A quadratic equation with real roots is given as: "
            "x^2 - 5x - 6 = 0. "
            "The sum and product of the roots are in the ratio 3:2. "
            "What is the value of one of the roots?"
        ),
        "topic": "Algebra",
        "difficulty": "Hard",
        "company": "TCS"
    }

    print("\nTest 3: Ambiguous Algebra Question")

    result = validate_question(bad_algebra_question)

    show_validation(result)

    # -----------------------------------------
    # TEST 4: MATHEMATICALLY INCONSISTENT
    # -----------------------------------------

    inconsistent_algebra_question = {
        "question": (
            "What is the value of x in the equation: "
            "2x^2 + 5x - 3 = 0, "
            "given that the sum of the roots of the "
            "quadratic equation is 5?"
        ),
        "topic": "Algebra",
        "difficulty": "Hard",
        "company": "TCS"
    }

    print("\nTest 4: Mathematically Inconsistent Algebra Question")

    result = validate_question(
        inconsistent_algebra_question
    )

    show_validation(result)
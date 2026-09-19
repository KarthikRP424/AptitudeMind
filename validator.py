import re
import math


# ============================================================
# MAIN QUESTION VALIDATOR
# ============================================================

def validate_question(question_data):
    """
    Validate the complete aptitude question structure
    and perform topic-specific mathematical checks.
    """

    errors = []

    # --------------------------------------------------------
    # Basic data validation
    # --------------------------------------------------------

    if not isinstance(question_data, dict):
        return {
            "valid": False,
            "errors": [
                "Question data must be a dictionary."
            ]
        }

    # --------------------------------------------------------
    # Question text
    # --------------------------------------------------------

    question = question_data.get("question", "")

    if not isinstance(question, str):
        errors.append(
            "Question text must be a string."
        )
        question = ""

    else:
        question = question.strip()

    if not question:
        errors.append(
            "Question text is missing."
        )

    # --------------------------------------------------------
    # Topic
    # --------------------------------------------------------

    topic = question_data.get("topic")

    if not topic:
        errors.append(
            "Topic is missing."
        )

    # --------------------------------------------------------
    # Difficulty
    # --------------------------------------------------------

    difficulty = question_data.get("difficulty")

    if difficulty not in [
        "Easy",
        "Medium",
        "Hard"
    ]:
        errors.append(
            "Invalid or missing difficulty."
        )

    # --------------------------------------------------------
    # Company
    # --------------------------------------------------------

    company = question_data.get("company")

    if not company:
        errors.append(
            "Company information is missing."
        )

    # --------------------------------------------------------
    # Options
    # --------------------------------------------------------

    options = question_data.get("options")

    if options is not None:

        if not isinstance(options, list):

            errors.append(
                "Options must be a list."
            )

        elif len(options) < 2:

            errors.append(
                "Question should contain at least two options."
            )

        else:

            # Make sure every option contains usable text.
            for index, option in enumerate(
                options,
                start=1
            ):

                if not isinstance(option, str):

                    errors.append(
                        f"Option {index} must be a string."
                    )

                elif not option.strip():

                    errors.append(
                        f"Option {index} is empty."
                    )

            # Detect duplicate options.
            cleaned_options = [
                option.strip().lower()
                for option in options
                if isinstance(option, str)
            ]

            if len(cleaned_options) != len(
                set(cleaned_options)
            ):

                errors.append(
                    "Options must be unique."
                )

    # --------------------------------------------------------
    # Minimum question length
    # --------------------------------------------------------

    if question and len(question) < 10:

        errors.append(
            "Question text is too short."
        )

    # --------------------------------------------------------
    # Ambiguous wording
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Topic-specific validation
    # --------------------------------------------------------

    if topic == "Algebra":

        errors.extend(
            validate_algebra_question(
                question,
                options
            )
        )

    if topic == "Percentage":

        errors.extend(
            validate_percentage_question(
                question
            )
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# ============================================================
# ALGEBRA VALIDATION
# ============================================================

def validate_algebra_question(
    question,
    options=None
):
    """
    Validate Algebra questions.

    Includes:
    - Ambiguous root detection
    - Quadratic equation extraction
    - Vieta sum verification
    - Vieta product verification
    - Discriminant verification
    - Quadratic option/answer verification
    """

    errors = []

    q = question.lower()

    # --------------------------------------------------------
    # Basic quadratic validation
    # --------------------------------------------------------

    if "quadratic equation" in q and "=" in question:

        root_keywords = [
            "roots",
            "root",
            "sum of the roots",
            "product of the roots",
            "discriminant"
        ]

        if not any(
            keyword in q
            for keyword in root_keywords
        ):

            errors.append(
                "Quadratic equation lacks clear root context."
            )

    # --------------------------------------------------------
    # Ambiguous root question
    # --------------------------------------------------------

    if "what is the value of one of the roots" in q:

        errors.append(
            "Question asks for 'one of the roots' "
            "without uniquely identifying a root."
        )

    # --------------------------------------------------------
    # Potentially unreliable ratio question
    # --------------------------------------------------------

    if (
        "sum and product of the roots" in q
        and "ratio" in q
    ):

        errors.append(
            "Root ratio question requires mathematical "
            "verification before being accepted."
        )

    # --------------------------------------------------------
    # Extract quadratic equation
    # --------------------------------------------------------

    quadratic_match = re.search(
        r"([+-]?\d*\.?\d*)\s*x\^2\s*"
        r"([+-]\s*\d*\.?\d*)\s*x\s*"
        r"([+-]\s*\d*\.?\d*)\s*=\s*0",
        question,
        re.IGNORECASE
    )

    if not quadratic_match:

        return errors

    # --------------------------------------------------------
    # Parse coefficients
    # --------------------------------------------------------

    a_text = quadratic_match.group(1)
    b_text = quadratic_match.group(2)
    c_text = quadratic_match.group(3)

    try:

        a = parse_coefficient(
            a_text,
            default=1
        )

        b = parse_coefficient(
            b_text,
            default=0
        )

        c = parse_coefficient(
            c_text,
            default=0
        )

    except ValueError:

        errors.append(
            "Unable to parse quadratic equation coefficients."
        )

        return errors

    # --------------------------------------------------------
    # Prevent invalid quadratic
    # --------------------------------------------------------

    if abs(a) < 0.000001:

        errors.append(
            "Coefficient of x² cannot be zero in a quadratic equation."
        )

        return errors

    # --------------------------------------------------------
    # Vieta: Sum of roots
    # --------------------------------------------------------

    expected_sum = -b / a

    sum_match = re.search(
        r"sum of (?:the )?roots"
        r"(?:.*?is|.*?=)\s*"
        r"(-?\d+(?:\.\d+)?)",
        q
    )

    if sum_match:

        claimed_sum = float(
            sum_match.group(1)
        )

        if abs(
            expected_sum - claimed_sum
        ) > 0.000001:

            errors.append(
                "Mathematical inconsistency: "
                f"sum of roots should be "
                f"{format_number(expected_sum)}, "
                f"not {format_number(claimed_sum)}."
            )

    # --------------------------------------------------------
    # Vieta: Product of roots
    # --------------------------------------------------------

    expected_product = c / a

    product_match = re.search(
        r"product of (?:the )?roots"
        r"(?:.*?is|.*?=)\s*"
        r"(-?\d+(?:\.\d+)?)",
        q
    )

    if product_match:

        claimed_product = float(
            product_match.group(1)
        )

        if abs(
            expected_product - claimed_product
        ) > 0.000001:

            errors.append(
                "Mathematical inconsistency: "
                "product of roots should be "
                f"{format_number(expected_product)}, "
                f"not {format_number(claimed_product)}."
            )

    # --------------------------------------------------------
    # Discriminant validation
    # --------------------------------------------------------

    expected_discriminant = (
        b ** 2
        - 4 * a * c
    )

    discriminant_match = re.search(
        r"discriminant"
        r"(?:.*?is|.*?=|.*?equals)"
        r"\s*(-?\d+(?:\.\d+)?)",
        q
    )

    if discriminant_match:

        claimed_discriminant = float(
            discriminant_match.group(1)
        )

        if abs(
            expected_discriminant
            - claimed_discriminant
        ) > 0.000001:

            errors.append(
                "Mathematical inconsistency: "
                "discriminant should be "
                f"{format_number(expected_discriminant)}, "
                f"not "
                f"{format_number(claimed_discriminant)}."
            )

    # --------------------------------------------------------
    # NEW: Verify quadratic options
    # --------------------------------------------------------

    if options:

        errors.extend(
            validate_quadratic_options(
                question=question,
                options=options,
                a=a,
                b=b,
                c=c
            )
        )

    return errors


# ============================================================
# QUADRATIC OPTION VALIDATION
# ============================================================

def validate_quadratic_options(
    question,
    options,
    a,
    b,
    c
):
    """
    Verify that options contain the mathematically correct
    answer for common quadratic 'find x' questions.

    This is intentionally limited to questions where the
    wording clearly asks for a value/root of x.

    It avoids trying to interpret arbitrary Algebra questions.
    """

    errors = []

    q = question.lower()

    # --------------------------------------------------------
    # Determine whether this is an x/root answer question
    # --------------------------------------------------------

    answer_question = any(
        phrase in q
        for phrase in [
            "what is the value of x",
            "find the value of x",
            "value of x",
            "solve for x",
            "find x",
            "solve the equation",
            "what are the roots",
            "find the roots"
        ]
    )

    if not answer_question:

        return errors

    # --------------------------------------------------------
    # Calculate discriminant
    # --------------------------------------------------------

    discriminant = (
        b ** 2
        - 4 * a * c
    )

    if discriminant < 0:

        # No real roots.
        # For ordinary multiple-choice aptitude questions,
        # at least one option should normally state that.
        real_root_phrases = [
            "no real roots",
            "no real solution",
            "no real value",
            "not real"
        ]

        option_text = " ".join(
            str(option).lower()
            for option in options
        )

        if not any(
            phrase in option_text
            for phrase in real_root_phrases
        ):

            errors.append(
                "Quadratic has no real roots, but "
                "the options do not contain a clear "
                "'no real roots' answer."
            )

        return errors

    # --------------------------------------------------------
    # Calculate roots
    # --------------------------------------------------------

    sqrt_discriminant = math.sqrt(
        discriminant
    )

    root_1 = (
        -b + sqrt_discriminant
    ) / (2 * a)

    root_2 = (
        -b - sqrt_discriminant
    ) / (2 * a)

    roots = [
        root_1,
        root_2
    ]

    # --------------------------------------------------------
    # Extract numeric values from options
    # --------------------------------------------------------

    numeric_options = []

    for option in options:

        parsed_value = parse_numeric_option(
            option
        )

        if parsed_value is not None:

            numeric_options.append(
                parsed_value
            )

    # --------------------------------------------------------
    # If no numeric options can be interpreted
    # --------------------------------------------------------

    if not numeric_options:

        errors.append(
            "Quadratic answer question has no "
            "recognizable numeric options."
        )

        return errors

    # --------------------------------------------------------
    # Check whether at least one option matches a root
    # --------------------------------------------------------

    has_correct_root = False

    for option_value in numeric_options:

        for root in roots:

            if approximately_equal(
                option_value,
                root
            ):

                has_correct_root = True
                break

        if has_correct_root:
            break

    if not has_correct_root:

        errors.append(
            "None of the provided options matches "
            "a correct root of the quadratic equation. "
            f"Expected roots: "
            f"{format_number(root_1)} and "
            f"{format_number(root_2)}."
        )

        return errors

    # --------------------------------------------------------
    # For a unique-root question, verify uniqueness
    # --------------------------------------------------------

    if approximately_equal(
        root_1,
        root_2
    ):

        matching_options = 0

        for option_value in numeric_options:

            if approximately_equal(
                option_value,
                root_1
            ):

                matching_options += 1

        if matching_options != 1:

            errors.append(
                "Quadratic has one repeated root, "
                "but the options do not contain "
                "exactly one matching answer."
            )

    return errors


# ============================================================
# NUMERIC OPTION PARSER
# ============================================================

def parse_numeric_option(option):
    """
    Convert common numeric option formats into float.

    Supported examples:
        '5'
        '-3'
        '0.5'
        '1/2'
        '-3/4'
        '5.0'
    """

    if not isinstance(
        option,
        str
    ):

        return None

    value = option.strip()

    if not value:

        return None

    # Remove common formatting.
    value = value.replace(
        ",",
        ""
    )

    # --------------------------------------------------------
    # Fraction
    # --------------------------------------------------------

    fraction_match = re.fullmatch(
        r"(-?\d+(?:\.\d+)?)\s*/\s*"
        r"(-?\d+(?:\.\d+)?)",
        value
    )

    if fraction_match:

        numerator = float(
            fraction_match.group(1)
        )

        denominator = float(
            fraction_match.group(2)
        )

        if abs(denominator) < 0.000001:

            return None

        return numerator / denominator

    # --------------------------------------------------------
    # Normal number
    # --------------------------------------------------------

    number_match = re.fullmatch(
        r"-?\d+(?:\.\d+)?",
        value
    )

    if number_match:

        return float(value)

    return None


# ============================================================
# APPROXIMATE NUMBER COMPARISON
# ============================================================

def approximately_equal(
    first,
    second,
    tolerance=0.000001
):
    """
    Compare floating-point values safely.
    """

    return abs(
        first - second
    ) <= tolerance


# ============================================================
# COEFFICIENT PARSER
# ============================================================

def parse_coefficient(
    value,
    default=0
):
    """
    Convert a coefficient string into a float.

    Examples:
        ''   -> default
        '+'  -> 1
        '-'  -> -1
        '5'  -> 5
        '-3' -> -3
    """

    value = value.strip().replace(
        " ",
        ""
    )

    if value in [
        "",
        "+"
    ]:

        return (
            default
            if value == ""
            else 1
        )

    if value == "-":

        return -1

    return float(value)


# ============================================================
# NUMBER FORMATTER
# ============================================================

def format_number(value):

    if value == int(value):

        return str(
            int(value)
        )

    return str(
        round(
            value,
            4
        )
    )


# ============================================================
# PERCENTAGE VALIDATION
# ============================================================

def validate_percentage_question(
    question
):

    errors = []

    q = question.lower()

    # --------------------------------------------------------
    # Percentage context
    # --------------------------------------------------------

    if not any(
        word in q
        for word in [
            "%",
            "percent",
            "percentage"
        ]
    ):

        errors.append(
            "Percentage topic question has "
            "no percentage context."
        )

    # --------------------------------------------------------
    # Discount validation
    # --------------------------------------------------------

    discount_words = [
        "discount",
        "discounted",
        "marked price",
        "selling price"
    ]

    if any(
        word in q
        for word in discount_words
    ):

        if "price" not in q:

            errors.append(
                "Discount question does not "
                "clearly identify a price."
            )

    return errors


# ============================================================
# DISPLAY VALIDATION
# ============================================================

def show_validation(result):

    print(
        "\n🛡️ Question Validation"
    )

    print(
        "----------------------"
    )

    if result["valid"]:

        print(
            "Status: ✅ VALID"
        )

    else:

        print(
            "Status: ❌ INVALID"
        )

        print(
            "\n⚠️ Errors:"
        )

        for error in result["errors"]:

            print(
                "-",
                error
            )


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Test 1
    # --------------------------------------------------------

    valid_question = {

        "question":
            "What is 25% of 200?",

        "topic":
            "Percentage",

        "difficulty":
            "Easy",

        "company":
            "TCS",

        "options":
            [
                "40",
                "50",
                "60",
                "70"
            ]
    }

    print(
        "\nTest 1: Valid Percentage Question"
    )

    result = validate_question(
        valid_question
    )

    show_validation(
        result
    )

    # --------------------------------------------------------
    # Test 2
    # --------------------------------------------------------

    invalid_question = {

        "question": "",

        "topic":
            "Percentage",

        "difficulty":
            "Unknown",

        "company":
            "",

        "options":
            [
                "100"
            ]
    }

    print(
        "\nTest 2: Invalid Question"
    )

    result = validate_question(
        invalid_question
    )

    show_validation(
        result
    )

    # --------------------------------------------------------
    # Test 3
    # --------------------------------------------------------

    bad_algebra_question = {

        "question": (
            "A quadratic equation with real roots "
            "is given as: "
            "x^2 - 5x - 6 = 0. "
            "The sum and product of the roots "
            "are in the ratio 3:2. "
            "What is the value of one of the roots?"
        ),

        "topic":
            "Algebra",

        "difficulty":
            "Hard",

        "company":
            "TCS"
    }

    print(
        "\nTest 3: Ambiguous Algebra Question"
    )

    result = validate_question(
        bad_algebra_question
    )

    show_validation(
        result
    )

    # --------------------------------------------------------
    # Test 4
    # --------------------------------------------------------

    inconsistent_algebra_question = {

        "question": (
            "What is the value of x in the equation: "
            "2x^2 + 5x - 3 = 0, "
            "given that the sum of the roots "
            "of the quadratic equation is 5?"
        ),

        "topic":
            "Algebra",

        "difficulty":
            "Hard",

        "company":
            "TCS"
    }

    print(
        "\nTest 4: Mathematically Inconsistent "
        "Algebra Question"
    )

    result = validate_question(
        inconsistent_algebra_question
    )

    show_validation(
        result
    )

    # --------------------------------------------------------
    # Test 5
    # --------------------------------------------------------

    bad_discriminant_question = {

        "question": (
            "What is the value of x in the equation: "
            "3x^2 + 5x - 8 = 0, "
            "given that the discriminant "
            "of the quadratic equation is 16?"
        ),

        "topic":
            "Algebra",

        "difficulty":
            "Hard",

        "company":
            "TCS"
    }

    print(
        "\nTest 5: Mathematically Inconsistent "
        "Discriminant"
    )

    result = validate_question(
        bad_discriminant_question
    )

    show_validation(
        result
    )

    # --------------------------------------------------------
    # Test 6 - NEW
    # --------------------------------------------------------

    invalid_options_question = {

        "question": (
            "What is the value of x in the equation: "
            "2x^2 + 5x - 3 = 0?"
        ),

        "topic":
            "Algebra",

        "difficulty":
            "Hard",

        "company":
            "TCS",

        "options":
            [
                "-1",
                "1",
                "3",
                "5"
            ]
    }

    print(
        "\nTest 6: Incorrect Algebra Options"
    )

    result = validate_question(
        invalid_options_question
    )

    show_validation(
        result
    )

    # --------------------------------------------------------
    # Test 7 - NEW
    # --------------------------------------------------------

    valid_options_question = {

        "question": (
            "What is the value of x in the equation: "
            "2x^2 + 5x - 3 = 0?"
        ),

        "topic":
            "Algebra",

        "difficulty":
            "Hard",

        "company":
            "TCS",

        "options":
            [
                "-3",
                "-1",
                "0.5",
                "5"
            ]
    }

    print(
        "\nTest 7: Correct Algebra Options"
    )

    result = validate_question(
        valid_options_question
    )

    show_validation(
        result
    )
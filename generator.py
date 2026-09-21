
import json
import math
import ollama

from validator import validate_question
from answer_engine import verify_answer


# ============================================================
# Configuration
# ============================================================

MODEL_NAME = "llama3.2:3b"
MAX_GENERATION_ATTEMPTS = 5


# ============================================================
# Generate Raw Question Using Ollama
# ============================================================

def generate_raw_question(topic, difficulty, company=None):

    company_text = company if company else "general placement"

    prompt = """
You are an expert aptitude question generator for a placement
preparation platform.

Create ONE aptitude question.

Requested Topic:
TOPIC_PLACEHOLDER

Requested Difficulty:
DIFFICULTY_PLACEHOLDER

Company Style:
COMPANY_PLACEHOLDER

Return ONLY valid JSON.

Required JSON format:

{
    "question": "question text",
    "type": "QUESTION_TYPE",
    "parameters": {
        "parameter_name": "parameter_value"
    },
    "options": [
        "option 1",
        "option 2",
        "option 3",
        "option 4"
    ]
}

============================================================
GENERAL RULES
============================================================

1. Create exactly ONE question.

2. The question must clearly belong to the requested topic.

3. Match the requested difficulty.

4. Provide exactly FOUR options.

5. There must be exactly one correct answer.

6. The correct answer MUST be present in the options.

7. The other three options must be plausible distractors.

8. Do NOT reveal which option is correct.

9. Do NOT provide an explanation.

10. Do NOT provide an answer field.

11. The "type" field must describe the mathematical
    question type.

12. The "parameters" field MUST contain all numerical
    information required for a deterministic Python program
    to calculate the answer.

13. The question text MUST match the parameters exactly.

14. Do not put calculated answers inside parameters.

15. Return JSON only.

============================================================
ALGEBRA RULES
============================================================

If the topic is Algebra, use ONLY:

1. LINEAR_EQUATION
2. QUADRATIC_EQUATION

------------------------------------------------------------
LINEAR_EQUATION
------------------------------------------------------------

Use:

ax + b = c

Parameters:

{
    "a": number,
    "b": number,
    "c": number
}

Rules:

- a must not be zero.
- Use integer coefficients.
- Prefer small coefficients.
- Prefer an integer value of x.
- The correct x MUST appear in the options.
- The equation and parameters MUST match.

Example:

{
    "question": "Solve for x: 3x + 4 = 13",
    "type": "LINEAR_EQUATION",
    "parameters": {
        "a": 3,
        "b": 4,
        "c": 13
    },
    "options": [
        "2",
        "3",
        "4",
        "5"
    ]
}

------------------------------------------------------------
QUADRATIC_EQUATION
------------------------------------------------------------

Use:

ax^2 + bx + c = 0

Parameters:

{
    "a": number,
    "b": number,
    "c": number
}

CRITICAL RULES:

- a must not be zero.
- Use integer coefficients.
- Use small or reasonable coefficients.
- The quadratic MUST have real roots.
- Prefer integer roots.
- Simple fractions such as 1/2 and -1/2 are allowed.
- DO NOT create irrational roots.
- DO NOT create quadratics with no real roots.
- DO NOT use complicated decimal roots.
- The equation and parameters MUST match.
- The correct root MUST appear in the options.
- If asking for both roots, both roots must appear.

GOOD EXAMPLE:

{
    "question": "Solve for x: 2x^2 - 7x + 3 = 0",
    "type": "QUADRATIC_EQUATION",
    "parameters": {
        "a": 2,
        "b": -7,
        "c": 3
    },
    "options": [
        "3",
        "1/2",
        "2",
        "4"
    ]
}

The roots are:

3 and 1/2

============================================================
ALGEBRA DIFFICULTY
============================================================

Hard difficulty does NOT mean irrational or unnecessarily
complicated mathematics.

Increase difficulty through:

- multi-step wording
- application-style questions
- slightly larger coefficients
- reasoning

Keep the underlying mathematics clean and deterministic.

============================================================
NON-ALGEBRA EXAMPLES
============================================================

PERCENTAGE:

{
    "question": "What is 20% of 200?",
    "type": "PERCENTAGE",
    "parameters": {
        "value": 200,
        "percentage": 20
    },
    "options": [
        "20",
        "40",
        "60",
        "80"
    ]
}

PROFIT:

{
    "question": "A product costs 1000 and is sold at a profit of 20%. What is the selling price?",
    "type": "PROFIT",
    "parameters": {
        "cost_price": 1000,
        "profit_percentage": 20
    },
    "options": [
        "1100",
        "1150",
        "1200",
        "1250"
    ]
}

AVERAGE:

{
    "question": "What is the average of 10, 20 and 30?",
    "type": "AVERAGE",
    "parameters": {
        "numbers": [10, 20, 30]
    },
    "options": [
        "15",
        "20",
        "25",
        "30"
    ]
}

SIMPLE INTEREST:

{
    "question": "Find the simple interest on 1000 at 10% per annum for 2 years.",
    "type": "SIMPLE_INTEREST",
    "parameters": {
        "principal": 1000,
        "rate": 10,
        "time": 2
    },
    "options": [
        "100",
        "150",
        "200",
        "250"
    ]
}

DISTANCE:

{
    "question": "A car travels at 60 km/h for 2 hours. What distance does it cover?",
    "type": "DISTANCE",
    "parameters": {
        "speed": 60,
        "time": 2
    },
    "options": [
        "100",
        "110",
        "120",
        "130"
    ]
}

============================================================
FINAL REQUIREMENT
============================================================

Create a NEW question.

Topic:
TOPIC_PLACEHOLDER

Difficulty:
DIFFICULTY_PLACEHOLDER

Company:
COMPANY_PLACEHOLDER

Return ONLY valid JSON.
"""

    # --------------------------------------------------------
    # Insert runtime values safely
    # --------------------------------------------------------

    prompt = prompt.replace(
        "TOPIC_PLACEHOLDER",
        str(topic)
    )

    prompt = prompt.replace(
        "DIFFICULTY_PLACEHOLDER",
        str(difficulty)
    )

    prompt = prompt.replace(
        "COMPANY_PLACEHOLDER",
        str(company_text)
    )

    # --------------------------------------------------------
    # Call Ollama
    # --------------------------------------------------------

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response["message"]["content"].strip()

    return content


# ============================================================
# Parse AI Response
# ============================================================

def parse_question_response(
    content,
    topic,
    difficulty,
    company=None
):

    try:

        data = json.loads(content)

    except json.JSONDecodeError as error:

        return {
            "valid": False,
            "errors": [
                f"AI returned invalid JSON: {error}"
            ]
        }

    if not isinstance(data, dict):

        return {
            "valid": False,
            "errors": [
                "AI response must be a JSON object."
            ]
        }

    # --------------------------------------------------------
    # Extract structured fields
    # --------------------------------------------------------

    question_text = data.get("question", "")
    question_type = data.get("type", "")
    parameters = data.get("parameters", {})
    options = data.get("options")

    # --------------------------------------------------------
    # Basic generator-level checks
    # --------------------------------------------------------

    errors = []

    if not isinstance(question_text, str) or not question_text.strip():

        errors.append(
            "Question must be a non-empty string."
        )

    if not isinstance(question_type, str) or not question_type.strip():

        errors.append(
            "Question type is missing."
        )

    if not isinstance(parameters, dict):

        errors.append(
            "Parameters must be a JSON object."
        )

    if not isinstance(options, list):

        errors.append(
            "Options must be a list."
        )

    elif len(options) != 4:

        errors.append(
            "Question must contain exactly four options."
        )

    # --------------------------------------------------------
    # Algebra structured validation
    # --------------------------------------------------------

    if (
        topic.lower() == "algebra"
        and isinstance(question_type, str)
    ):

        normalized_type = question_type.strip().upper()

        allowed_types = {
            "LINEAR_EQUATION",
            "QUADRATIC_EQUATION"
        }

        if normalized_type not in allowed_types:

            errors.append(
                "Algebra question type must be "
                "LINEAR_EQUATION or QUADRATIC_EQUATION."
            )

        else:

            required_parameters = [
                "a",
                "b",
                "c"
            ]

            for parameter in required_parameters:

                if parameter not in parameters:

                    errors.append(
                        f"Algebra parameter "
                        f"'{parameter}' is missing."
                    )

            # ------------------------------------------------
            # Linear validation
            # ------------------------------------------------

            if normalized_type == "LINEAR_EQUATION":

                try:

                    a = float(
                        parameters.get("a", 0)
                    )

                    if a == 0:

                        errors.append(
                            "Linear coefficient 'a' "
                            "cannot be zero."
                        )

                except (TypeError, ValueError):

                    errors.append(
                        "Linear coefficient 'a' "
                        "must be numeric."
                    )

            # ------------------------------------------------
            # Quadratic validation
            # ------------------------------------------------

            if normalized_type == "QUADRATIC_EQUATION":

                try:

                    a = float(
                        parameters.get("a", 0)
                    )

                    b = float(
                        parameters.get("b", 0)
                    )

                    c = float(
                        parameters.get("c", 0)
                    )

                    if a == 0:

                        errors.append(
                            "Quadratic coefficient 'a' "
                            "cannot be zero."
                        )

                    else:

                        discriminant = (
                            b * b
                            - 4 * a * c
                        )

                        # ------------------------------------
                        # Reject no-real-root equations
                        # ------------------------------------

                        if discriminant < 0:

                            errors.append(
                                "Quadratic must have real roots."
                            )

                        else:

                            sqrt_d = math.sqrt(
                                discriminant
                            )

                            root1 = (
                                -b + sqrt_d
                            ) / (2 * a)

                            root2 = (
                                -b - sqrt_d
                            ) / (2 * a)

                            # --------------------------------
                            # Accept integer or half roots
                            # --------------------------------

                            def is_clean_root(root):

                                integer_root = math.isclose(
                                    root,
                                    round(root),
                                    abs_tol=1e-9
                                )

                                half_root = math.isclose(
                                    root * 2,
                                    round(root * 2),
                                    abs_tol=1e-9
                                )

                                return (
                                    integer_root
                                    or half_root
                                )

                            if not is_clean_root(root1):

                                errors.append(
                                    "Quadratic root is not a "
                                    "clean integer or simple "
                                    "half fraction."
                                )

                            if not is_clean_root(root2):

                                errors.append(
                                    "Quadratic root is not a "
                                    "clean integer or simple "
                                    "half fraction."
                                )

                except (TypeError, ValueError):

                    errors.append(
                        "Quadratic coefficients must "
                        "be numeric."
                    )

    # --------------------------------------------------------
    # Stop if basic structure is invalid
    # --------------------------------------------------------

    if errors:

        return {
            "valid": False,
            "errors": errors
        }

    # --------------------------------------------------------
    # Normalize structured fields
    # --------------------------------------------------------

    question_data = {

        "question": question_text.strip(),

        "topic": topic,

        "difficulty": difficulty,

        "company": (
            company
            if company
            else "general placement"
        ),

        "type": question_type.strip().upper(),

        "parameters": parameters,

        "options": options
    }

    return {

        "valid": True,

        "question_data": question_data
    }


# ============================================================
# Generate and Validate Question
# ============================================================

def generate_question(
    topic,
    difficulty="Easy",
    company=None
):

    print(
        "\n🤖 AptitudeMind AI Question Generator"
    )

    print(
        "====================================="
    )

    for attempt in range(
        1,
        MAX_GENERATION_ATTEMPTS + 1
    ):

        print(
            f"\n🤖 Generating question "
            f"(Attempt {attempt}/{MAX_GENERATION_ATTEMPTS})..."
        )

        # ----------------------------------------------------
        # Generate
        # ----------------------------------------------------

        raw_question = generate_raw_question(
            topic=topic,
            difficulty=difficulty,
            company=company
        )

        # ----------------------------------------------------
        # Parse
        # ----------------------------------------------------

        parsed = parse_question_response(
            content=raw_question,
            topic=topic,
            difficulty=difficulty,
            company=company
        )

        if not parsed["valid"]:

            print(
                "❌ Question failed basic parsing."
            )

            for error in parsed["errors"]:

                print(
                    "   -",
                    error
                )

            continue

        question_data = parsed["question_data"]

        # ----------------------------------------------------
        # Validator
        # ----------------------------------------------------

        validation = validate_question(
            question_data
        )

        if not validation["valid"]:

            print(
                "❌ Question failed validation."
            )

            for error in validation["errors"]:

                print(
                    "   -",
                    error
                )

            continue

        # ----------------------------------------------------
        # Answer Engine
        # ----------------------------------------------------

        verification = verify_answer(
            question_data
        )

        if verification["status"] != "success":

            print(
                "❌ Answer Engine verification failed."
            )

            print(
                "   -",
                verification.get(
                    "message",
                    "Unknown verification error"
                )
            )

            continue

        # ----------------------------------------------------
        # Success
        # ----------------------------------------------------

        print(
            "✅ Question passed validation."
        )

        print(
            "✅ Answer Engine verification passed."
        )

        return question_data

    # --------------------------------------------------------
    # Generation failed
    # --------------------------------------------------------

    print(
        "\n⚠️ Unable to generate a valid question "
        "after maximum attempts."
    )

    return None


# ============================================================
# Display Question
# ============================================================

def display_question(question):

    print(
        "\n📚 Generated Question"
    )

    print(
        "-------------------------------------"
    )

    print(
        question["question"]
    )

    print(
        "\nOptions:"
    )

    for index, option in enumerate(
        question["options"],
        start=1
    ):

        print(
            f"{index}. {option}"
        )

    print(
        "\nTopic:",
        question["topic"]
    )

    print(
        "Type:",
        question["type"]
    )

    print(
        "Difficulty:",
        question["difficulty"]
    )

    print(
        "Company:",
        question["company"]
    )

    print(
        "\nParameters:"
    )

    print(
        json.dumps(
            question["parameters"],
            indent=4
        )
    )


# ============================================================
# Test Generator
# ============================================================

if __name__ == "__main__":

    question = generate_question(
        topic="Algebra",
        difficulty="Hard",
        company="TCS"
    )

    if question:

        display_question(
            question
        )

    else:

        print(
            "\n❌ AptitudeMind could not generate "
            "a verified question."
        )

# ============================================================
# AptitudeMind - AI Question Generator
# ============================================================

import json
import ollama

from validator import validate_question


# ============================================================
# Configuration
# ============================================================

MODEL_NAME = "llama3.2:3b"
MAX_GENERATION_ATTEMPTS = 3


# ============================================================
# Generate Raw Question Using Ollama
# ============================================================

def generate_raw_question(topic, difficulty, company=None):

    company_text = company if company else "general placement"

    prompt = f"""
You are an expert aptitude question generator for a placement
preparation platform.

Create ONE {difficulty}-level aptitude question.

Requested Topic:
{topic}

Company Style:
{company_text}

Return ONLY valid JSON.

Required JSON format:

{{
    "question": "question text",

    "type": "QUESTION_TYPE",

    "parameters": {{
        "parameter_name": "parameter_value"
    }},

    "options": [
        "option 1",
        "option 2",
        "option 3",
        "option 4"
    ]
}}

IMPORTANT:

1. Create exactly ONE question.

2. The question must clearly belong to the requested topic.

3. The question must match the requested difficulty.

4. The question must have exactly ONE correct answer.

5. Provide exactly FOUR options.

6. The correct answer MUST be present in the four options.

7. The other three options must be plausible distractors.

8. Do NOT reveal which option is correct.

9. Do NOT provide an explanation.

10. Do NOT provide an answer field.

11. The "type" field must describe the mathematical question type.

12. The "parameters" field MUST contain the numerical
    information required to independently calculate the answer.

13. The parameters must be sufficient for a deterministic
    Python program to calculate the correct answer.

14. Do not put calculations inside the parameters.

15. Do not use random or missing parameter values.

16. Keep parameter names simple and descriptive.

17. Return JSON only.

------------------------------------------------------------
EXAMPLE 1 - PERCENTAGE
------------------------------------------------------------

{{
    "question": "What is 20% of 200?",

    "type": "PERCENTAGE",

    "parameters": {{
        "value": 200,
        "percentage": 20
    }},

    "options": [
        "20",
        "40",
        "60",
        "80"
    ]
}}

------------------------------------------------------------
EXAMPLE 2 - PROFIT
------------------------------------------------------------

{{
    "question": "A product costs 1000 and is sold at a profit of 20%. What is the selling price?",

    "type": "PROFIT",

    "parameters": {{
        "cost_price": 1000,
        "profit_percentage": 20
    }},

    "options": [
        "1100",
        "1150",
        "1200",
        "1250"
    ]
}}

------------------------------------------------------------
EXAMPLE 3 - AVERAGE
------------------------------------------------------------

{{
    "question": "What is the average of 10, 20 and 30?",

    "type": "AVERAGE",

    "parameters": {{
        "numbers": [10, 20, 30]
    }},

    "options": [
        "15",
        "20",
        "25",
        "30"
    ]
}}

------------------------------------------------------------
EXAMPLE 4 - SIMPLE INTEREST
------------------------------------------------------------

{{
    "question": "Find the simple interest on 1000 at 10% per annum for 2 years.",

    "type": "SIMPLE_INTEREST",

    "parameters": {{
        "principal": 1000,
        "rate": 10,
        "time": 2
    }},

    "options": [
        "100",
        "150",
        "200",
        "250"
    ]
}}

------------------------------------------------------------
EXAMPLE 5 - TIME SPEED DISTANCE
------------------------------------------------------------

{{
    "question": "A car travels at 60 km/h for 2 hours. What distance does it cover?",

    "type": "DISTANCE",

    "parameters": {{
        "speed": 60,
        "time": 2
    }},

    "options": [
        "100",
        "110",
        "120",
        "130"
    ]
}}

------------------------------------------------------------

Do not copy these examples.

Create a NEW question based on:

Topic: {topic}
Difficulty: {difficulty}
Company: {company_text}

Return ONLY JSON.
"""

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
    difficulty,
    company=None
):

    for attempt in range(
        1,
        MAX_GENERATION_ATTEMPTS + 1
    ):

        print(
            f"\n🤖 Generating question "
            f"(Attempt {attempt}/{MAX_GENERATION_ATTEMPTS})..."
        )

        # ----------------------------------------------------
        # Ask Ollama
        # ----------------------------------------------------

        raw_response = generate_raw_question(

            topic=topic,

            difficulty=difficulty,

            company=company
        )

        # ----------------------------------------------------
        # Parse response
        # ----------------------------------------------------

        parsed = parse_question_response(

            content=raw_response,

            topic=topic,

            difficulty=difficulty,

            company=company
        )

        # ----------------------------------------------------
        # Parsing failed
        # ----------------------------------------------------

        if not parsed["valid"]:

            print(
                "❌ AI response failed "
                "generator-level checks."
            )

            for error in parsed["errors"]:

                print(
                    f"   - {error}"
                )

            continue

        # ----------------------------------------------------
        # Extract question
        # ----------------------------------------------------

        question_data = parsed["question_data"]

        # ----------------------------------------------------
        # Existing Validator
        # ----------------------------------------------------

        validation_result = validate_question(
            question_data
        )

        if validation_result["valid"]:

            print(
                "✅ Question passed validation."
            )

            return question_data

        # ----------------------------------------------------
        # Validation failed
        # ----------------------------------------------------

        print(
            "❌ Question failed validation."
        )

        for error in validation_result["errors"]:

            print(
                f"   - {error}"
            )

    # ========================================================
    # Maximum attempts reached
    # ========================================================

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

    print(
        "🤖 AptitudeMind AI Question Generator"
    )

    print(
        "====================================="
    )

    question = generate_question(

        topic="Algebra",

        difficulty="Hard",

        company="TCS"
    )

    if question:

        display_question(question)

    else:

        print(
            "\n❌ AptitudeMind could not generate "
            "a verified question."
        )
# ============================================================
# AptitudeMind - Question Validator
# ============================================================


# ============================================================
# Basic Question Validation
# ============================================================

def validate_question(question_data):
    """
    Validate the basic structure of an AI-generated question.

    Returns:
        {
            "valid": True/False,
            "errors": [...]
        }
    """

    errors = []

    # --------------------------------------------------------
    # Check question text
    # --------------------------------------------------------

    question = question_data.get("question", "").strip()

    if not question:
        errors.append("Question text is missing.")

    # --------------------------------------------------------
    # Check topic
    # --------------------------------------------------------

    topic = question_data.get("topic")

    if not topic:
        errors.append("Topic is missing.")

    # --------------------------------------------------------
    # Check difficulty
    # --------------------------------------------------------

    difficulty = question_data.get("difficulty")

    if difficulty not in ["Easy", "Medium", "Hard"]:
        errors.append("Invalid or missing difficulty.")

    # --------------------------------------------------------
    # Check company
    # --------------------------------------------------------

    company = question_data.get("company")

    if not company:
        errors.append("Company information is missing.")

    # --------------------------------------------------------
    # Check options
    # --------------------------------------------------------

    options = question_data.get("options")

    if options is not None:

        if not isinstance(options, list):
            errors.append("Options must be a list.")

        elif len(options) < 2:
            errors.append("Question should contain at least two options.")

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# ============================================================
# Display Validation Result
# ============================================================

def show_validation(result):

    print("\n🔍 AptitudeMind Question Validator")
    print("=================================")

    if result["valid"]:
        print("✅ Question passed basic validation.")
    else:
        print("❌ Question failed validation.")

        print("\n⚠️ Problems found:")

        for error in result["errors"]:
            print(" -", error)


# ============================================================
# Test Validator
# ============================================================

if __name__ == "__main__":

    print("🧠 Testing AptitudeMind Validator")

    # --------------------------------------------------------
    # Test 1: Valid question
    # --------------------------------------------------------

    valid_question = {
        "question": "What is 20% of 500?",
        "topic": "Percentage",
        "difficulty": "Easy",
        "company": "TCS",
        "options": [
            "50",
            "100",
            "150",
            "200"
        ]
    }

    result = validate_question(valid_question)

    print("\nTest 1:")
    show_validation(result)

    # --------------------------------------------------------
    # Test 2: Invalid question
    # --------------------------------------------------------

    invalid_question = {
        "question": "",
        "topic": "Algebra",
        "difficulty": "Very Hard",
        "company": "",
        "options": [
            "1"
        ]
    }

    result = validate_question(invalid_question)

    print("\nTest 2:")
    show_validation(result)
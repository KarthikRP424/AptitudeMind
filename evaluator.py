"""
AptitudeMind - Answer Evaluator

Responsibilities:
1. Validate question structure.
2. Adapt generated question data for Answer Engine.
3. Display a validated question.
4. Accept the student's answer.
5. Ask the deterministic Answer Engine to verify the answer.
6. Determine correct / incorrect.
7. Return a structured evaluation result.
8. Display the verified explanation.

Architecture:

    Generator
        ↓
    Question
        ↓
    Evaluator Adapter
        ↓
    Answer Engine
        ↓
    Verified Correct Answer
        ↓
    Student Answer
        ↓
    Evaluation
        ↓
    Result

This module does NOT generate questions.
This module does NOT calculate aptitude answers itself.
This module does NOT modify progress or memory yet.
"""


from answer_engine import verify_answer
from memory import record_result

TEST_MODE = False


# ============================================================
# QUESTION STRUCTURE VALIDATION
# ============================================================

def validate_question_structure(question_data):
    """
    Validate the basic structure of a generated question.

    The Generator stores mathematical parameters inside:

        question_data["parameters"]

    The Answer Engine currently expects those parameters at
    the top level.

    This function only validates the general question structure.
    It does NOT verify the mathematical answer.
    """

    if not isinstance(question_data, dict):

        return {
            "status": "error",
            "valid": False,
            "message": "Question data must be a dictionary."
        }

    if not question_data.get("question"):

        return {
            "status": "error",
            "valid": False,
            "message": "Question text is missing."
        }

    options = question_data.get("options")

    if not isinstance(options, list):

        return {
            "status": "error",
            "valid": False,
            "message": "Question options must be a list."
        }

    if len(options) != 4:

        return {
            "status": "error",
            "valid": False,
            "message": "Question must contain exactly four options."
        }

    for option in options:

        if option is None or str(option).strip() == "":

            return {
                "status": "error",
                "valid": False,
                "message": "Question contains an empty option."
            }

    parameters = question_data.get("parameters")

    if parameters is not None and not isinstance(parameters, dict):

        return {
            "status": "error",
            "valid": False,
            "message": "Question parameters must be a dictionary."
        }

    return {
        "status": "success",
        "valid": True,
        "message": "Question structure is valid."
    }


# ============================================================
# ADAPT QUESTION FOR ANSWER ENGINE
# ============================================================

def prepare_for_answer_engine(question_data):
    """
    Convert the Generator's question format into the format
    expected by Answer Engine.

    Generator format:

        {
            "question": "...",
            "topic": "Percentage",
            "type": "PERCENTAGE",
            "parameters": {
                "value": 200,
                "percentage": 20
            },
            "options": [...]
        }

    Answer Engine format:

        {
            "question": "...",
            "topic": "Percentage",
            "type": "PERCENTAGE",
            "value": 200,
            "percentage": 20,
            "options": [...]
        }

    The existing Answer Engine expects mathematical parameters
    at the top level.

    Returns:
        dict: Answer Engine compatible question.
    """

    prepared_question = dict(question_data)

    parameters = question_data.get("parameters", {})

    if not isinstance(parameters, dict):

        parameters = {}

    # --------------------------------------------------------
    # Copy generated parameters to top level
    # --------------------------------------------------------

    for key, value in parameters.items():

        prepared_question[key] = value

    # --------------------------------------------------------
    # Preserve important metadata
    # --------------------------------------------------------

    if "topic" in question_data:

        prepared_question["topic"] = question_data["topic"]

    if "type" in question_data:

        prepared_question["type"] = question_data["type"]

    if "options" in question_data:

        prepared_question["options"] = question_data["options"]

    # --------------------------------------------------------
    # Time-Speed-Distance compatibility
    # --------------------------------------------------------
    #
    # Answer Engine expects:
    #
    #     question_type = distance / speed / time
    #
    # Some generated questions may store this inside:
    #
    #     parameters["question_type"]
    #
    # or use:
    #
    #     type = DISTANCE / SPEED / TIME
    #
    # Normalize both possibilities.
    # --------------------------------------------------------

    if "question_type" not in prepared_question:

        if "question_type" in parameters:

            prepared_question["question_type"] = (
                parameters["question_type"]
            )

        elif isinstance(
            question_data.get("type"),
            str
        ):

            question_type = question_data["type"].strip().lower()

            if question_type in {
                "distance",
                "speed",
                "time"
            }:

                prepared_question["question_type"] = (
                    question_type
                )

    return prepared_question


# ============================================================
# DISPLAY QUESTION
# ============================================================

def display_question(question_data):
    """
    Display the question and its options.

    The correct answer is intentionally NOT displayed.
    """

    print("\n" + "=" * 60)
    print("📝 APTITUDE QUESTION")
    print("=" * 60)

    print("\nQuestion:")
    print(question_data["question"])

    print("\nOptions:")

    options = question_data.get("options", [])

    for index, option in enumerate(options, start=1):

        print(f"{index}. {option}")

    print("\n" + "-" * 60)


# ============================================================
# GET STUDENT ANSWER
# ============================================================

def get_student_answer():
    """
    Ask the student to select an option.

    Returns:
        int: Selected option number (1-4)
    """

    while True:

        answer = input("👉 Your answer (1-4): ").strip()

        if not answer.isdigit():

            print(
                "⚠️ Please enter a number between 1 and 4."
            )

            continue

        answer = int(answer)

        if answer not in range(1, 5):

            print(
                "⚠️ Please choose only 1, 2, 3, or 4."
            )

            continue

        return answer


# ============================================================
# EVALUATE ANSWER
# ============================================================

def evaluate_answer(question_data, student_answer, save_progress=True):
    """
    Evaluate the student's answer.

    The Answer Engine determines the mathematically verified
    correct option.

    The Evaluator compares that verified option with the
    student's selected option.

    Returns:
        dict: Structured evaluation result.
    """

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    structure = validate_question_structure(
        question_data
    )

    if not structure["valid"]:

        return {
            "status": "error",
            "result": None,
            "student_answer": student_answer,
            "correct_answer": None,
            "calculated_answer": None,
            "explanation": "",
            "message": structure["message"]
        }

    # --------------------------------------------------------
    # Validate student answer
    # --------------------------------------------------------

    if not isinstance(student_answer, int):

        return {
            "status": "error",
            "result": None,
            "student_answer": student_answer,
            "correct_answer": None,
            "calculated_answer": None,
            "explanation": "",
            "message": "Student answer must be an integer."
        }

    if student_answer not in range(1, 5):

        return {
            "status": "error",
            "result": None,
            "student_answer": student_answer,
            "correct_answer": None,
            "calculated_answer": None,
            "explanation": "",
            "message": (
                "Student answer must be between 1 and 4."
            )
        }

    # --------------------------------------------------------
    # Prepare Answer Engine input
    # --------------------------------------------------------

    answer_engine_question = prepare_for_answer_engine(
        question_data
    )

    # --------------------------------------------------------
    # Ask Answer Engine to verify
    # --------------------------------------------------------

    print(
        "\n🧮 Answer Engine verifying "
        "the correct answer..."
    )

    verification = verify_answer(
        answer_engine_question
    )

    # --------------------------------------------------------
    # Handle Answer Engine error
    # --------------------------------------------------------

    if verification.get("status") != "success":

        return {
            "status": "error",
            "result": None,
            "student_answer": student_answer,
            "correct_answer": None,
            "calculated_answer": verification.get(
                "calculated_answer"
            ),
            "explanation": verification.get(
                "explanation",
                ""
            ),
            "message": (
                "Answer Engine could not verify "
                "the question: "
                + verification.get(
                    "message",
                    "Unknown verification error."
                )
            )
        }

    # --------------------------------------------------------
    # Read verified correct answer
    # --------------------------------------------------------

    correct_answer = verification.get(
        "correct_answer"
    )

    # --------------------------------------------------------
    # Answer Engine currently returns an integer
    # for normal single-answer questions.
    # --------------------------------------------------------

    if not isinstance(correct_answer, int):

        return {
            "status": "error",
            "result": None,
            "student_answer": student_answer,
            "correct_answer": None,
            "calculated_answer": verification.get(
                "calculated_answer"
            ),
            "explanation": verification.get(
                "explanation",
                ""
            ),
            "message": (
                "Answer Engine returned an invalid "
                "correct option."
            )
        }

    if correct_answer not in range(1, 5):

        return {
            "status": "error",
            "result": None,
            "student_answer": student_answer,
            "correct_answer": None,
            "calculated_answer": verification.get(
                "calculated_answer"
            ),
            "explanation": verification.get(
                "explanation",
                ""
            ),
            "message": (
                "Verified correct answer must "
                "be between 1 and 4."
            )
        }

    # --------------------------------------------------------
    # Compare answers
    # --------------------------------------------------------

    if student_answer == correct_answer:

        result = "correct"

        message = "Correct answer! 🎉"

    else:

        result = "incorrect"

        message = "Incorrect answer."

    # --------------------------------------------------------
    # Record progress
    # --------------------------------------------------------

    if save_progress and not TEST_MODE:
        record_result(
            question_data["topic"],
            result == "correct"
        )

    # --------------------------------------------------------
    # Return structured result
    # --------------------------------------------------------

    return {
        "status": "success",
        "result": result,
        "student_answer": student_answer,
        "correct_answer": correct_answer,
        "calculated_answer": verification.get(
            "calculated_answer"
        ),
        "explanation": verification.get(
            "explanation",
            ""
        ),
        "message": message
    }


# ============================================================
# SHOW RESULT
# ============================================================

def show_result(question_data, evaluation):
    """
    Display the evaluation result to the student.
    """

    print("\n" + "=" * 60)
    print("📊 EVALUATION RESULT")
    print("=" * 60)

    if evaluation["status"] != "success":

        print("\n❌ Evaluation Error")

        print(
            evaluation["message"]
        )

        return

    # --------------------------------------------------------
    # Correct
    # --------------------------------------------------------

    if evaluation["result"] == "correct":

        print("\n✅ CORRECT!")

        print(
            "Excellent work! 🎉"
        )

    # --------------------------------------------------------
    # Incorrect
    # --------------------------------------------------------

    else:

        print("\n❌ INCORRECT")

        correct_answer = (
            evaluation["correct_answer"]
        )

        options = question_data.get(
            "options",
            []
        )

        if 1 <= correct_answer <= len(options):

            print(
                f"Correct option: "
                f"{correct_answer}. "
                f"{options[correct_answer - 1]}"
            )

    # --------------------------------------------------------
    # Answer information
    # --------------------------------------------------------

    print(
        "\nYour answer:",
        evaluation["student_answer"]
    )

    print(
        "Correct answer:",
        evaluation["correct_answer"]
    )

    # --------------------------------------------------------
    # Calculated answer
    # --------------------------------------------------------

    if evaluation.get(
        "calculated_answer"
    ) is not None:

        print(
            "Calculated answer:",
            evaluation["calculated_answer"]
        )

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    explanation = evaluation.get(
        "explanation"
    )

    if explanation:

        print("\n💡 Explanation:")

        print(explanation)


# ============================================================
# COMPLETE QUESTION EVALUATION
# ============================================================

def evaluate_question(question_data):
    """
    Complete student interaction.

    Flow:

        Validate question
                ↓
        Display question
                ↓
        Student selects option
                ↓
        Adapt question format
                ↓
        Answer Engine verification
                ↓
        Compare answer
                ↓
        Show result

    Returns:
        dict: Structured evaluation result.
    """

    structure = validate_question_structure(
        question_data
    )

    if not structure["valid"]:

        result = {
            "status": "error",
            "result": None,
            "student_answer": None,
            "correct_answer": None,
            "calculated_answer": None,
            "explanation": "",
            "message": structure["message"]
        }

        print(
            "\n❌ Invalid question:"
        )

        print(
            result["message"]
        )

        return result

    display_question(
        question_data
    )

    student_answer = get_student_answer()

    evaluation = evaluate_answer(
        question_data,
        student_answer
    )

    show_result(
        question_data,
        evaluation
    )

    return evaluation


# ============================================================
# TESTS
# ============================================================

def run_tests():

    # Tests should verify evaluation logic without changing the user's
    # real progress.json file.
    global TEST_MODE
    TEST_MODE = True

    print("\n🧪 AptitudeMind Evaluator Tests")
    print("=" * 60)

    # --------------------------------------------------------
    # Test 1 - Percentage
    # --------------------------------------------------------

    print("\nTest 1: Percentage - Correct")

    percentage_question = {
        "question": "What is 20% of 200?",
        "topic": "Percentage",
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

    result = evaluate_answer(
        percentage_question,
        2
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"
    assert result["correct_answer"] == 2

    print("✅ Test 1 passed.")

    # --------------------------------------------------------
    # Test 2 - Percentage incorrect
    # --------------------------------------------------------

    print("\nTest 2: Percentage - Incorrect")

    result = evaluate_answer(
        percentage_question,
        3
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "incorrect"
    assert result["correct_answer"] == 2

    print("✅ Test 2 passed.")

    # --------------------------------------------------------
    # Test 3 - Profit
    # --------------------------------------------------------

    print("\nTest 3: Profit")

    profit_question = {
        "question": (
            "An item costs 1000 and is sold at "
            "20% profit. Find the selling price."
        ),
        "topic": "Profit",
        "type": "PROFIT",
        "parameters": {
            "cost_price": 1000,
            "profit_percentage": 20
        },
        "options": [
            "1100",
            "1200",
            "1300",
            "1400"
        ]
    }

    result = evaluate_answer(
        profit_question,
        2
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"
    assert result["correct_answer"] == 2

    print("✅ Test 3 passed.")

    # --------------------------------------------------------
    # Test 4 - Loss
    # --------------------------------------------------------

    print("\nTest 4: Loss")

    loss_question = {
        "question": (
            "An item costs 1000 and is sold at "
            "20% loss. Find the selling price."
        ),
        "topic": "Loss",
        "type": "LOSS",
        "parameters": {
            "cost_price": 1000,
            "loss_percentage": 20
        },
        "options": [
            "700",
            "800",
            "900",
            "1200"
        ]
    }

    result = evaluate_answer(
        loss_question,
        2
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"
    assert result["correct_answer"] == 2

    print("✅ Test 4 passed.")

    # --------------------------------------------------------
    # Test 5 - Average
    # --------------------------------------------------------

    print("\nTest 5: Average")

    average_question = {
        "question": (
            "Find the average of 10, 20 and 30."
        ),
        "topic": "Average",
        "type": "AVERAGE",
        "parameters": {
            "numbers": [
                10,
                20,
                30
            ]
        },
        "options": [
            "10",
            "20",
            "30",
            "40"
        ]
    }

    result = evaluate_answer(
        average_question,
        2
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"
    assert result["correct_answer"] == 2

    print("✅ Test 5 passed.")

    # --------------------------------------------------------
    # Test 6 - Simple Interest
    # --------------------------------------------------------

    print("\nTest 6: Simple Interest")

    simple_interest_question = {
        "question": (
            "Find the simple interest on 1000 "
            "at 10% per year for 2 years."
        ),
        "topic": "Simple Interest",
        "type": "SIMPLE_INTEREST",
        "parameters": {
            "principal": 1000,
            "rate": 10,
            "time": 2
        },
        "options": [
            "100",
            "200",
            "300",
            "400"
        ]
    }

    result = evaluate_answer(
        simple_interest_question,
        2
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"
    assert result["correct_answer"] == 2

    print("✅ Test 6 passed.")

    # --------------------------------------------------------
    # Test 7 - Distance
    # --------------------------------------------------------

    print("\nTest 7: Distance")

    distance_question = {
        "question": (
            "A vehicle travels at 60 km/h "
            "for 2 hours. Find the distance."
        ),
        "topic": "Time-Speed-Distance",
        "type": "DISTANCE",
        "parameters": {
            "speed": 60,
            "time": 2,
            "question_type": "distance"
        },
        "options": [
            "60",
            "100",
            "120",
            "150"
        ]
    }

    result = evaluate_answer(
        distance_question,
        3
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"
    assert result["correct_answer"] == 3

    print("✅ Test 7 passed.")

    # --------------------------------------------------------
    # Test 8 - Speed
    # --------------------------------------------------------

    print("\nTest 8: Speed")

    speed_question = {
        "question": (
            "A vehicle travels 120 km in 2 hours. "
            "Find its speed."
        ),
        "topic": "Time-Speed-Distance",
        "type": "SPEED",
        "parameters": {
            "distance": 120,
            "time": 2,
            "question_type": "speed"
        },
        "options": [
            "40",
            "60",
            "80",
            "100"
        ]
    }

    result = evaluate_answer(
        speed_question,
        2
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"
    assert result["correct_answer"] == 2

    print("✅ Test 8 passed.")

    # --------------------------------------------------------
    # Test 9 - Time
    # --------------------------------------------------------

    print("\nTest 9: Time")

    time_question = {
        "question": (
            "A vehicle travels 120 km at 60 km/h. "
            "Find the time taken."
        ),
        "topic": "Time-Speed-Distance",
        "type": "TIME",
        "parameters": {
            "distance": 120,
            "speed": 60,
            "question_type": "time"
        },
        "options": [
            "1",
            "2",
            "3",
            "4"
        ]
    }

    result = evaluate_answer(
        time_question,
        2
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"
    assert result["correct_answer"] == 2

    print("✅ Test 9 passed.")

    # --------------------------------------------------------
    # Test 10 - Quadratic Equation
    # --------------------------------------------------------

    print("\nTest 10: Quadratic Equation")

    quadratic_question = {
        "question": (
            "Solve for x: "
            "2x^2 + 5x - 3 = 0"
        ),
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

    result = evaluate_answer(
        quadratic_question,
        1
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"
    assert result["correct_answer"] == 1

    print("✅ Test 10 passed.")

    # --------------------------------------------------------
    # Test 11 - Invalid student answer
    # --------------------------------------------------------

    print("\nTest 11: Invalid student answer")

    result = evaluate_answer(
        percentage_question,
        5
    )

    print(result)

    assert result["status"] == "error"
    assert result["result"] is None

    print("✅ Test 11 passed.")

    # --------------------------------------------------------
    # Test 12 - Missing question
    # --------------------------------------------------------

    print("\nTest 12: Missing question text")

    incomplete_question = {
        "topic": "Percentage",
        "options": [
            "10",
            "20",
            "30",
            "40"
        ]
    }

    result = evaluate_answer(
        incomplete_question,
        2
    )

    print(result)

    assert result["status"] == "error"

    print("✅ Test 12 passed.")

    # --------------------------------------------------------
    # Test 13 - Invalid option count
    # --------------------------------------------------------

    print("\nTest 13: Invalid option count")

    invalid_options_question = {
        "question": "What is 10 + 10?",
        "topic": "Percentage",
        "options": [
            "10",
            "20",
            "30"
        ]
    }

    result = evaluate_answer(
        invalid_options_question,
        2
    )

    print(result)

    assert result["status"] == "error"

    print("✅ Test 13 passed.")

    # --------------------------------------------------------
    # Test 14 - Unsupported topic
    # --------------------------------------------------------

    print("\nTest 14: Unsupported topic")

    unsupported_question = {
        "question": "Who is the founder of XYZ?",
        "topic": "General Knowledge",
        "type": "GENERAL_KNOWLEDGE",
        "options": [
            "Person A",
            "Person B",
            "Person C",
            "Person D"
        ]
    }

    result = evaluate_answer(
        unsupported_question,
        1
    )

    print(result)

    assert result["status"] == "error"

    print("✅ Test 14 passed.")

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("🎉 ALL EVALUATOR TESTS PASSED")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_tests()
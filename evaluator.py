"""
AptitudeMind - Answer Evaluator

Responsibilities:
1. Display a validated question.
2. Display four options.
3. Accept the student's answer.
4. Validate the input.
5. Determine correct / incorrect.
6. Return a structured evaluation result.

This module does NOT generate questions.
This module does NOT modify progress or memory yet.
Those will be connected in the next stage.
"""


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


def get_student_answer():
    """
    Ask the student to select an option.

    Returns:
        int: Selected option number (1-4)
    """

    while True:

        answer = input("👉 Your answer (1-4): ").strip()

        if not answer.isdigit():
            print("⚠️ Please enter a number between 1 and 4.")
            continue

        answer = int(answer)

        if answer not in range(1, 5):
            print("⚠️ Please choose only 1, 2, 3, or 4.")
            continue

        return answer


def evaluate_answer(question_data, student_answer):
    """
    Compare the student's answer with the verified correct answer.

    Expected question_data structure:

    {
        "question": "...",
        "options": ["...", "...", "...", "..."],
        "correct_answer": 2
    }

    Returns a structured evaluation dictionary.
    """

    if "correct_answer" not in question_data:
        return {
            "status": "error",
            "result": None,
            "student_answer": student_answer,
            "correct_answer": None,
            "message": (
                "Question does not contain a verified correct answer."
            )
        }

    correct_answer = question_data["correct_answer"]

    if not isinstance(correct_answer, int):
        return {
            "status": "error",
            "result": None,
            "student_answer": student_answer,
            "correct_answer": None,
            "message": (
                "Correct answer must be an integer between 1 and 4."
            )
        }

    if correct_answer not in range(1, 5):
        return {
            "status": "error",
            "result": None,
            "student_answer": student_answer,
            "correct_answer": None,
            "message": (
                "Correct answer must be between 1 and 4."
            )
        }

    if student_answer == correct_answer:

        return {
            "status": "success",
            "result": "correct",
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "message": "Correct answer! 🎉"
        }

    return {
        "status": "success",
        "result": "incorrect",
        "student_answer": student_answer,
        "correct_answer": correct_answer,
        "message": "Incorrect answer."
    }


def show_result(question_data, evaluation):
    """
    Display the evaluation result to the student.
    """

    print("\n" + "=" * 60)
    print("📊 EVALUATION RESULT")
    print("=" * 60)

    if evaluation["status"] != "success":

        print("\n❌ Evaluation Error")
        print(evaluation["message"])
        return

    if evaluation["result"] == "correct":

        print("\n✅ CORRECT!")
        print("Excellent work! 🎉")

    else:

        print("\n❌ INCORRECT")

        correct_answer = evaluation["correct_answer"]

        options = question_data.get("options", [])

        if 1 <= correct_answer <= len(options):

            print(
                f"Correct option: "
                f"{correct_answer}. "
                f"{options[correct_answer - 1]}"
            )

    print("\nYour answer:",
          evaluation["student_answer"])

    print("Correct answer:",
          evaluation["correct_answer"])


def evaluate_question(question_data):
    """
    Complete student interaction.

    Flow:

        Display question
            ↓
        Student selects option
            ↓
        Evaluate answer
            ↓
        Show result

    Returns:
        evaluation dictionary
    """

    if not isinstance(question_data, dict):

        return {
            "status": "error",
            "result": None,
            "student_answer": None,
            "correct_answer": None,
            "message": "Question data must be a dictionary."
        }

    if not question_data.get("question"):

        return {
            "status": "error",
            "result": None,
            "student_answer": None,
            "correct_answer": None,
            "message": "Question text is missing."
        }

    options = question_data.get("options")

    if not isinstance(options, list):

        return {
            "status": "error",
            "result": None,
            "student_answer": None,
            "correct_answer": None,
            "message": "Question options must be a list."
        }

    if len(options) != 4:

        return {
            "status": "error",
            "result": None,
            "student_answer": None,
            "correct_answer": None,
            "message": "Question must contain exactly four options."
        }

    if "correct_answer" not in question_data:

        return {
            "status": "error",
            "result": None,
            "student_answer": None,
            "correct_answer": None,
            "message": (
                "Question does not contain a verified correct answer."
            )
        }

    display_question(question_data)

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

    print("\n🧪 AptitudeMind Evaluator Tests")
    print("=" * 60)

    test_question = {
        "question": "What is 20% of 200?",
        "options": [
            "20",
            "40",
            "60",
            "80"
        ],
        "correct_answer": 2
    }

    # --------------------------------------------------------
    # Test 1 - Correct answer
    # --------------------------------------------------------

    print("\nTest 1: Correct answer")

    result = evaluate_answer(
        test_question,
        2
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "correct"

    print("✅ Test 1 passed.")

    # --------------------------------------------------------
    # Test 2 - Incorrect answer
    # --------------------------------------------------------

    print("\nTest 2: Incorrect answer")

    result = evaluate_answer(
        test_question,
        3
    )

    print(result)

    assert result["status"] == "success"
    assert result["result"] == "incorrect"

    print("✅ Test 2 passed.")

    # --------------------------------------------------------
    # Test 3 - Invalid student answer
    # --------------------------------------------------------

    print("\nTest 3: Invalid student answer")

    result = evaluate_answer(
        test_question,
        5
    )

    print(result)

    # evaluate_answer expects the caller to validate input,
    # so this test confirms the comparison result itself.
    assert result["status"] == "success"
    assert result["result"] == "incorrect"

    print("✅ Test 3 passed.")

    # --------------------------------------------------------
    # Test 4 - Missing correct answer
    # --------------------------------------------------------

    print("\nTest 4: Missing correct answer")

    incomplete_question = {
        "question": "What is 10 + 10?",
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

    print("✅ Test 4 passed.")

    # --------------------------------------------------------
    # Test 5 - Invalid correct answer
    # --------------------------------------------------------

    print("\nTest 5: Invalid correct answer")

    invalid_question = {
        "question": "What is 10 + 10?",
        "options": [
            "10",
            "20",
            "30",
            "40"
        ],
        "correct_answer": 7
    }

    result = evaluate_answer(
        invalid_question,
        2
    )

    print(result)

    assert result["status"] == "error"

    print("✅ Test 5 passed.")

    print("\n" + "=" * 60)
    print("🎉 ALL EVALUATOR TESTS PASSED")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_tests()
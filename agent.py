# ============================================================
# AptitudeMind - Agent Decision & Execution Layer
# ============================================================

from search_engine import find_questions
from question_bank import search_questions
from difficulty import get_difficulty
from generator import generate_question
from validator import validate_question
from evaluator import evaluate_question


# ============================================================
# Agent Decision
# ============================================================

def decide_action(
    query=None,
    topic=None,
    company=None,
    difficulty=None
):
    """
    Decide what AptitudeMind should do.

    Decision flow:

        User Request
             ↓
        Search / Topic
             ↓
        Adaptive Difficulty
             ↓
        Retrieve or Generate
    """

    # --------------------------------------------------------
    # CASE 1: User provided a search query
    # --------------------------------------------------------

    if query:

        filters, questions = find_questions(query)

        # Check whether the search detected
        # at least one useful filter.
        has_filter = any(
            value is not None
            for value in filters.values()
        )

        if not has_filter:

            return {
                "action": "ask",
                "filters": filters,
                "questions": []
            }

        # ----------------------------------------------------
        # Adaptive Difficulty
        # ----------------------------------------------------

        # If the user did NOT explicitly provide
        # a difficulty, let the Agent determine it
        # from student performance.

        if (
            filters["topic"]
            and filters["difficulty"] is None
        ):

            filters["difficulty"] = get_difficulty(
                filters["topic"]
            )

            print(
                "\n🧠 Adaptive difficulty selected:",
                filters["difficulty"]
            )

            # Search again using the adaptive difficulty.
            questions = search_questions(
                company=filters["company"],
                topic=filters["topic"],
                difficulty=filters["difficulty"]
            )

        # ----------------------------------------------------
        # Question found
        # ----------------------------------------------------

        if questions:

            return {
                "action": "retrieve",
                "filters": filters,
                "questions": questions
            }

        # ----------------------------------------------------
        # No question found
        # ----------------------------------------------------

        return {
            "action": "generate",
            "filters": filters,
            "questions": []
        }

    # --------------------------------------------------------
    # CASE 2: Topic provided directly
    # --------------------------------------------------------

    if topic:

        selected_difficulty = difficulty

        # If difficulty was not explicitly supplied,
        # determine it from student performance.
        if selected_difficulty is None:

            selected_difficulty = get_difficulty(
                topic
            )

        return {
            "action": "generate",
            "filters": {
                "company": company,
                "topic": topic,
                "difficulty": selected_difficulty
            },
            "questions": []
        }

    # --------------------------------------------------------
    # CASE 3: Nothing useful provided
    # --------------------------------------------------------

    return {
        "action": "ask",
        "filters": {},
        "questions": []
    }


# ============================================================
# Agent Execution
# ============================================================

def execute_decision(decision):
    """
    Execute the action selected by the Agent.

    Possible actions:

        retrieve
        generate
        ask
    """

    action = decision["action"]
    filters = decision["filters"]
    questions = decision["questions"]

    # ========================================================
    # RETRIEVE
    # ========================================================

    if action == "retrieve":

        if not questions:

            return {
                "status": "error",
                "action": "retrieve",
                "question": None,
                "message": "No question available."
            }

        question = questions[0]

        # Final validation of retrieved question
        validation = validate_question(question)

        if not validation["valid"]:

            return {
                "status": "error",
                "action": "retrieve",
                "question": None,
                "message": (
                    "Retrieved question failed validation."
                ),
                "validation_errors": validation["errors"]
            }

        return {
            "status": "success",
            "action": "retrieve",
            "question": question,
            "message": (
                "Question retrieved and validated "
                "from question bank."
            )
        }

    # ========================================================
    # GENERATE
    # ========================================================

    if action == "generate":

        topic = filters.get("topic")
        difficulty = filters.get("difficulty")
        company = filters.get("company")

        if not topic:

            return {
                "status": "error",
                "action": "generate",
                "question": None,
                "message": (
                    "Topic is required for generation."
                )
            }

        print(
            "\n🧠 Agent requesting a validated "
            "question from generator..."
        )

        generated_question = generate_question(
            topic=topic,
            difficulty=difficulty,
            company=company
        )

        if generated_question is None:

            return {
                "status": "error",
                "action": "generate",
                "question": None,
                "message": (
                    "AI failed to generate a valid "
                    "question after maximum generation attempts."
                )
            }

        if not isinstance(generated_question, dict):

            return {
                "status": "error",
                "action": "generate",
                "question": None,
                "message": (
                    "Generator returned an unexpected "
                    "question format."
                )
            }

        print(
            "\n🛡️ Agent performing final validation..."
        )

        validation = validate_question(
            generated_question
        )

        if not validation["valid"]:

            return {
                "status": "error",
                "action": "generate",
                "question": None,
                "message": (
                    "Generated question failed "
                    "final agent validation."
                ),
                "validation_errors": validation["errors"]
            }

        print("🛡️ Agent validation: PASSED")

        return {
            "status": "success",
            "action": "generate",
            "question": generated_question,
            "message": (
                "Question generated by Ollama, "
                "validated by generator, and "
                "verified by Agent."
            )
        }

    # ========================================================
    # ASK
    # ========================================================

    if action == "ask":

        return {
            "status": "waiting",
            "action": "ask",
            "question": None,
            "message": (
                "Please provide a topic, company, "
                "or search request."
            )
        }

    # ========================================================
    # UNKNOWN ACTION
    # ========================================================

    return {
        "status": "error",
        "action": action,
        "question": None,
        "message": (
            f"Unknown agent action: {action}"
        )
    }


# ============================================================
# Display Decision
# ============================================================

def show_decision(decision):

    print("\n🤖 AptitudeMind Agent")
    print("---------------------")

    print(
        "Action:",
        decision["action"]
    )

    print(
        "Filters:",
        decision["filters"]
    )

    print(
        "Questions found:",
        len(decision["questions"])
    )


# ============================================================
# Display Execution Result
# ============================================================

def show_execution_result(result):

    print("\n⚙️ Execution Result")
    print("-------------------")

    print(
        "Status:",
        result["status"]
    )

    print(
        "Action:",
        result["action"]
    )

    print(
        "Message:",
        result["message"]
    )

    # --------------------------------------------------------
    # Display Question
    # --------------------------------------------------------

    if result.get("question"):

        question = result["question"]

        print("\n📚 Question:")
        print(
            question["question"]
        )

        # ----------------------------------------------------
        # Options
        # ----------------------------------------------------

        if question.get("options"):

            print("\nOptions:")

            for index, option in enumerate(
                question["options"],
                start=1
            ):

                print(
                    f"{index}. {option}"
                )

        # ----------------------------------------------------
        # Metadata
        # ----------------------------------------------------

        print(
            "\nTopic:",
            question["topic"]
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
            "Source:",
            question.get(
                "source",
                "ai_generated"
            )
        )

    # --------------------------------------------------------
    # Validation Errors
    # --------------------------------------------------------

    if result.get("validation_errors"):

        print(
            "\n⚠️ Validation Errors:"
        )

        for error in result["validation_errors"]:

            print(
                "-",
                error
            )


# ============================================================
# Program Entry Point
# ============================================================

if __name__ == "__main__":

    print("🧠 AptitudeMind Agent")

    query = input(
        "\n🔎 Enter your request: "
    )

    decision = decide_action(
        query=query
    )

    show_decision(
        decision
    )

    result = execute_decision(
        decision
    )

    show_execution_result(
        result
    )

    # --------------------------------------------------------
    # Student Evaluation
    # --------------------------------------------------------

    if (
        result.get("status") == "success"
        and result.get("question")
    ):

        print(
            "\n🎯 Starting student evaluation..."
        )

        evaluation = evaluate_question(
            result["question"]
        )

        print(
            "\n🧠 Evaluation completed."
        )
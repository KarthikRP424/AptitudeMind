from search_engine import find_questions
from difficulty import get_difficulty
from generator import generate_question
from validator import validate_question


MAX_VALIDATION_ATTEMPTS = 3


def decide_action(query=None, topic=None, company=None, difficulty=None):
    """
    Decide what AptitudeMind should do.
    """

    if query:
        filters, questions = find_questions(query)

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

        if questions:
            return {
                "action": "retrieve",
                "filters": filters,
                "questions": questions
            }

        return {
            "action": "generate",
            "filters": filters,
            "questions": []
        }

    if topic:
        selected_difficulty = difficulty

        if selected_difficulty is None:
            selected_difficulty = get_difficulty(topic)

        return {
            "action": "generate",
            "filters": {
                "company": company,
                "topic": topic,
                "difficulty": selected_difficulty
            },
            "questions": []
        }

    return {
        "action": "ask",
        "filters": {},
        "questions": []
    }


def execute_decision(decision):
    """
    Execute the action selected by the agent.
    """

    action = decision["action"]
    filters = decision["filters"]
    questions = decision["questions"]

    # -----------------------------------------
    # RETRIEVE
    # -----------------------------------------

    if action == "retrieve":

        if not questions:
            return {
                "status": "error",
                "action": "retrieve",
                "question": None,
                "message": "No question available."
            }

        question = questions[0]

        validation = validate_question(question)

        if not validation["valid"]:
            return {
                "status": "error",
                "action": "retrieve",
                "question": None,
                "message": "Retrieved question failed validation.",
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

    # -----------------------------------------
    # GENERATE
    # -----------------------------------------

    if action == "generate":

        topic = filters.get("topic")
        difficulty = filters.get("difficulty")
        company = filters.get("company")

        if not topic:
            return {
                "status": "error",
                "action": "generate",
                "question": None,
                "message": "Topic is required for generation."
            }

        print(
            "\n🧠 Agent requesting a validated question "
            "from generator..."
        )

        generated_question = generate_question(
            topic=topic,
            difficulty=difficulty,
            company=company
        )

        # -----------------------------------------
        # GENERATOR FAILURE
        # -----------------------------------------

        if generated_question is None:

            return {
                "status": "error",
                "action": "generate",
                "question": None,
                "message": (
                    "AI failed to generate a valid question "
                    "after maximum generation attempts."
                )
            }

        # -----------------------------------------
        # SAFETY CHECK
        # -----------------------------------------

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

        # -----------------------------------------
        # FINAL AGENT VALIDATION
        # -----------------------------------------

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

    # -----------------------------------------
    # ASK
    # -----------------------------------------

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

    # -----------------------------------------
    # UNKNOWN ACTION
    # -----------------------------------------

    return {
        "status": "error",
        "action": action,
        "question": None,
        "message": f"Unknown agent action: {action}"
    }


def show_decision(decision):
    """
    Display the agent's decision.
    """

    print("\n🤖 AptitudeMind Agent")
    print("---------------------")
    print("Action:", decision["action"])
    print("Filters:", decision["filters"])
    print("Questions found:", len(decision["questions"]))


def show_execution_result(result):
    """
    Display execution result.
    """

    print("\n⚙️ Execution Result")
    print("-------------------")
    print("Status:", result["status"])
    print("Action:", result["action"])
    print("Message:", result["message"])

    if result.get("generation_attempts"):
        print(
            "Generation attempts:",
            result["generation_attempts"]
        )

    if result.get("question"):

        print("\n📚 Question:")
        print(result["question"]["question"])

        if result["question"].get("options"):

            print("\nOptions:")

            for index, option in enumerate(
                result["question"]["options"],
                start=1
            ):
                print(f"{index}. {option}")

        print(
            "\nTopic:",
            result["question"]["topic"]
        )

        print(
            "Difficulty:",
            result["question"]["difficulty"]
        )

        print(
            "Company:",
            result["question"]["company"]
        )

        print(
            "Source:",
            result["question"].get(
                "source",
                "ai_generated"
            )
        )

    if result.get("validation_errors"):

        print("\n⚠️ Validation Errors:")

        for error in result["validation_errors"]:
            print("-", error)


if __name__ == "__main__":

    print("🧠 AptitudeMind Agent")

    query = input(
        "\n🔎 Enter your request: "
    )

    decision = decide_action(
        query=query
    )

    show_decision(decision)

    result = execute_decision(
        decision
    )

    show_execution_result(result)
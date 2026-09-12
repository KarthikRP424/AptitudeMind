# ============================================================
# AptitudeMind - Agent Decision Layer
# ============================================================

from search_engine import find_questions
from difficulty import get_difficulty


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
    Decide what AptitudeMind should do next.

    Priority:

    1. Search for a matching question.
    2. If a question exists -> retrieve it.
    3. If no question exists -> generate a new question.
    """

    # --------------------------------------------------------
    # If the user provides a search query
    # --------------------------------------------------------

    if query:

        filters, questions = find_questions(query)

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

    # --------------------------------------------------------
    # If topic is provided directly
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # No information provided
    # --------------------------------------------------------

    return {
        "action": "ask",
        "filters": {},
        "questions": []
    }


# ============================================================
# Display Agent Decision
# ============================================================

def show_decision(decision):

    print("\n🤖 AptitudeMind Agent")
    print("====================")

    action = decision["action"]

    if action == "retrieve":

        print("🧠 Decision: RETRIEVE")
        print("📚 Matching question found.")

    elif action == "generate":

        print("🧠 Decision: GENERATE")
        print("🤖 No suitable question found.")
        print("   LLM should generate a new question.")

    elif action == "ask":

        print("🧠 Decision: ASK")
        print("❓ More information is required.")

    print("\n🔎 Filters:")

    filters = decision["filters"]

    print(
        "🏢 Company:",
        filters.get("company") or "Any"
    )

    print(
        "📚 Topic:",
        filters.get("topic") or "Any"
    )

    print(
        "🎯 Difficulty:",
        filters.get("difficulty") or "Any"
    )

    if decision["questions"]:

        print(
            "\n✅ Questions available:",
            len(decision["questions"])
        )


# ============================================================
# Test Agent
# ============================================================

if __name__ == "__main__":

    print("🧠 AptitudeMind Agent Decision System")

    query = input(
        "\n🔎 Enter request: "
    )

    decision = decide_action(query=query)

    show_decision(decision)
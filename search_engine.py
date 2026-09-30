# ============================================================
# AptitudeMind - Search Engine
# ============================================================

from search import parse_search
from question_bank import search_questions


# ============================================================
# Search Aptitude Questions
# ============================================================

def find_questions(query):
    """
    Convert a user's search query into filters
    and return matching aptitude questions.

    Example:

        TCS percentage medium

    becomes:

        Company    -> TCS
        Topic      -> Percentage
        Difficulty -> Medium

    Specific question types are also supported.

    Example:

        profit percentage

    becomes:

        Topic          -> Profit and Loss
        Question Type  -> PROFIT_PERCENTAGE
    """

    filters = parse_search(query)

    questions = search_questions(
        company=filters["company"],
        topic=filters["topic"],
        difficulty=filters["difficulty"]
    )

    # --------------------------------------------------------
    # Filter by specific question type
    #
    # The question bank already filters by:
    #
    # company + topic + difficulty
    #
    # We apply question type here because the existing
    # question_bank search interface does not require
    # modification.
    # --------------------------------------------------------

    question_type = filters.get("question_type")

    if question_type:

        questions = [
            question
            for question in questions
            if question.get("type") == question_type
        ]

    return filters, questions


# ============================================================
# Display Questions
# ============================================================

def display_questions(filters, questions):

    print("\n🧠 AptitudeMind Search Results")
    print("================================")

    print(
        "🏢 Company:",
        filters["company"]
        if filters["company"]
        else "All Companies"
    )

    print(
        "📚 Topic:",
        filters["topic"]
        if filters["topic"]
        else "All Topics"
    )

    print(
        "🎯 Difficulty:",
        filters["difficulty"]
        if filters["difficulty"]
        else "All Levels"
    )

    print(
        "🧩 Question Type:",
        filters["question_type"]
        if filters.get("question_type")
        else "All Types"
    )

    print("\n--------------------------------")

    if not questions:

        print("❌ No matching questions found.")
        return

    print(
        f"✅ {len(questions)} question(s) found."
    )

    print("--------------------------------")

    for index, question in enumerate(
        questions,
        start=1
    ):

        print(
            f"\n{index}. "
            f"{question['question']}"
        )

        print(
            f"   Company: {question['company']}"
        )

        print(
            f"   Topic: {question['topic']}"
        )

        print(
            f"   Type: {question['type']}"
        )

        print(
            f"   Difficulty: "
            f"{question['difficulty']}"
        )

        print(
            f"   Source: {question['source']}"
        )


# ============================================================
# Interactive Search
# ============================================================

def run_search():

    print("\n🤖 AptitudeMind Search Engine")
    print("==============================")

    query = input(
        "\n🔎 Search aptitude questions: "
    )

    filters, questions = find_questions(query)

    display_questions(
        filters,
        questions
    )


# ============================================================
# Program Entry Point
# ============================================================

if __name__ == "__main__":

    run_search()
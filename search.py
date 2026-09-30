# ============================================================
# AptitudeMind - Smart Search System
# ============================================================

from companies import get_companies
from topics import get_sections, get_available_topics
from difficulty import get_difficulty_levels


# ============================================================
# Normalize Text
# ============================================================

def normalize(text):
    """
    Convert text into a simple searchable format.
    """

    return text.lower().strip()


# ============================================================
# Find Company
# ============================================================

def find_company(query):
    """
    Find a company mentioned in the search query.

    Example:
        "tcs percentage medium"
        -> "TCS"
    """

    query = normalize(query)

    for company in get_companies():

        if company.lower() in query:

            return company

    return None


# ============================================================
# Find Difficulty
# ============================================================

def find_difficulty(query):
    """
    Find difficulty mentioned in the search query.

    Returns:
        Easy
        Medium
        Hard
        None
    """

    query = normalize(query)

    for difficulty in get_difficulty_levels():

        if difficulty.lower() in query:

            return difficulty

    return None


# ============================================================
# Find Question Type
# ============================================================

def find_question_type(query):
    """
    Find a specific question type mentioned
    in the search query.

    Examples:

        "profit percentage"
            -> PROFIT_PERCENTAGE

        "profit"
            -> PROFIT

        "loss"
            -> LOSS
    """

    query = normalize(query)

    question_type_aliases = {
        "profit percentage": "PROFIT_PERCENTAGE",
        "profit and percentage": "PROFIT_PERCENTAGE",
        "profit": "PROFIT",
        "loss": "LOSS"
    }

    # --------------------------------------------------------
    # Check longer phrases first.
    # --------------------------------------------------------

    sorted_aliases = sorted(
        question_type_aliases.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for alias, question_type in sorted_aliases:

        if alias in query:

            return question_type

    return None


# ============================================================
# Find Topic
# ============================================================

def find_topic(query):
    """
    Find an aptitude topic mentioned in the query.

    Supports both:
        1. Exact topic names
        2. Common topic aliases

    Examples:
        "percentage"
            -> Percentage

        "profit"
            -> Profit and Loss

        "loss"
            -> Profit and Loss

        "profit percentage"
            -> Profit and Loss
    """

    query = normalize(query)

    all_topics = get_available_topics()

    # --------------------------------------------------------
    # Topic aliases
    # --------------------------------------------------------

    topic_aliases = {
        "profit": "Profit and Loss",
        "loss": "Profit and Loss",
        "profit percentage": "Profit and Loss"
    }

    # --------------------------------------------------------
    # Check aliases first.
    # --------------------------------------------------------

    sorted_aliases = sorted(
        topic_aliases.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for alias, topic in sorted_aliases:

        if alias in query:

            if topic in all_topics:

                return topic

    # --------------------------------------------------------
    # Sort by length.
    # --------------------------------------------------------

    all_topics = sorted(
        all_topics,
        key=len,
        reverse=True
    )

    # --------------------------------------------------------
    # Exact topic matching
    # --------------------------------------------------------

    for topic in all_topics:

        if topic.lower() in query:

            return topic

    return None


# ============================================================
# Parse Search Query
# ============================================================

def parse_search(query):
    """
    Convert a natural search query into:

        company
        topic
        difficulty
        question_type
    """

    return {
        "company": find_company(query),
        "topic": find_topic(query),
        "difficulty": find_difficulty(query),
        "question_type": find_question_type(query)
    }


# ============================================================
# Validate Search
# ============================================================

def validate_search(search_data):
    """
    Check whether the parsed search contains
    at least one useful filter.
    """

    return any(
        value is not None
        for value in search_data.values()
    )


# ============================================================
# Display Search Result
# ============================================================

def show_search_result(search_data):
    """
    Display the parsed search information.
    """

    print("\n🔎 AptitudeMind Search")
    print("----------------------")

    print(
        "🏢 Company:",
        search_data["company"]
        if search_data["company"]
        else "All Companies"
    )

    print(
        "📚 Topic:",
        search_data["topic"]
        if search_data["topic"]
        else "All Topics"
    )

    print(
        "🎯 Difficulty:",
        search_data["difficulty"]
        if search_data["difficulty"]
        else "All Levels"
    )

    print(
        "🧩 Question Type:",
        search_data["question_type"]
        if search_data["question_type"]
        else "All Types"
    )


# ============================================================
# Test Search System
# ============================================================

if __name__ == "__main__":

    print("🧠 AptitudeMind Search System")

    query = input(
        "\n🔎 Enter your search: "
    )

    search_data = parse_search(query)

    show_search_result(search_data)
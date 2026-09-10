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
# Find Topic
# ============================================================

def find_topic(query):
    """
    Find an aptitude topic mentioned in the query.
    """

    query = normalize(query)

    all_topics = get_available_topics()

    # --------------------------------------------------------
    # Sort by length.
    #
    # This helps match longer topics first.
    #
    # Example:
    # "Time Speed and Distance"
    # should be checked before "Time".
    # --------------------------------------------------------

    all_topics = sorted(
        all_topics,
        key=len,
        reverse=True
    )

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

    Example:

        "TCS percentage medium"

    becomes:

        {
            "company": "TCS",
            "topic": "Percentage",
            "difficulty": "Medium"
        }
    """

    return {
        "company": find_company(query),
        "topic": find_topic(query),
        "difficulty": find_difficulty(query)
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


# ============================================================
# Test Search System
# ============================================================

if __name__ == "__main__":

    print("🧠 AptitudeMind Search System")

    query = input(
        "\n🔎 Enter your search: "
    )

    result = parse_search(query)

    if validate_search(result):

        show_search_result(result)

    else:

        print(
            "\n⚠️ No company, topic, or difficulty "
            "was detected."
        )
# ============================================================
# AptitudeMind - Difficulty System
# ============================================================


from memory import load_memory


# ------------------------------------------------------------
# Available Difficulty Levels
# ------------------------------------------------------------

DIFFICULTY_LEVELS = [
    "Easy",
    "Medium",
    "Hard"
]


# ------------------------------------------------------------
# Get All Difficulty Levels
# ------------------------------------------------------------

def get_difficulty_levels():
    """
    Return all available difficulty levels.
    """

    return DIFFICULTY_LEVELS


# ------------------------------------------------------------
# Validate Difficulty
# ------------------------------------------------------------

def is_valid_difficulty(difficulty):
    """
    Check whether a difficulty level is valid.
    """

    return difficulty in DIFFICULTY_LEVELS


# ------------------------------------------------------------
# Get Adaptive Difficulty
# ------------------------------------------------------------

def get_difficulty(topic):

    memory = load_memory()

    topic_data = memory["topics"].get(topic)

    # --------------------------------------------------------
    # No previous attempts
    # --------------------------------------------------------

    if not topic_data or topic_data["attempted"] == 0:
        return "Easy"

    # --------------------------------------------------------
    # Calculate accuracy
    # --------------------------------------------------------

    attempted = topic_data["attempted"]
    correct = topic_data["correct"]

    accuracy = (correct / attempted) * 100

    # --------------------------------------------------------
    # Adaptive difficulty rules
    # --------------------------------------------------------

    if accuracy < 50:
        return "Easy"

    elif accuracy <= 75:
        return "Medium"

    else:
        return "Hard"
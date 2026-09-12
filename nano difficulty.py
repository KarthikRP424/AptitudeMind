from memory import load_memory


def get_difficulty(topic):

    memory = load_memory()

    topic_data = memory["topics"].get(topic)

    if not topic_data or topic_data["attempted"] == 0:
        return "Easy"

    attempted = topic_data["attempted"]
    correct = topic_data["correct"]

    accuracy = (correct / attempted) * 100

    if accuracy < 50:
        return "Easy"

    elif accuracy <= 75:
        return "Medium"

    else:
        return "Hard"
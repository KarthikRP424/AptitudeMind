import json
import os


MEMORY_FILE = "progress.json"


def default_memory():

    return {
        "total": 0,
        "correct": 0,
        "wrong": 0,
        "topics": {}
    }


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return default_memory()

    try:

        with open(MEMORY_FILE, "r") as file:
            memory = json.load(file)

        # Upgrade old memory files
        if "topics" not in memory:
            memory["topics"] = {}

        return memory

    except (json.JSONDecodeError, OSError):

        return default_memory()


def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:

        json.dump(
            memory,
            file,
            indent=4
        )


def record_result(topic, is_correct):

    memory = load_memory()

    # Overall progress
    memory["total"] += 1

    if is_correct:
        memory["correct"] += 1
    else:
        memory["wrong"] += 1

    # Create topic if it doesn't exist
    if topic not in memory["topics"]:

        memory["topics"][topic] = {
            "attempted": 0,
            "correct": 0,
            "wrong": 0
        }

    # Topic progress
    memory["topics"][topic]["attempted"] += 1

    if is_correct:

        memory["topics"][topic]["correct"] += 1

    else:

        memory["topics"][topic]["wrong"] += 1

    save_memory(memory)


def show_progress():

    memory = load_memory()

    print("\n🧠 AptitudeMind Progress")
    print("------------------------")

    print(
        "Questions attempted:",
        memory["total"]
    )

    print(
        "Correct answers:",
        memory["correct"]
    )

    print(
        "Wrong answers:",
        memory["wrong"]
    )

    if memory["total"] > 0:

        accuracy = (
            memory["correct"]
            / memory["total"]
            * 100
        )

        print(
            "Overall accuracy:",
            round(accuracy, 2),
            "%"
        )

    # ---------------------------------------
    # Topic Performance
    # ---------------------------------------

    if memory["topics"]:

        print("\n📚 Topic Performance")
        print("--------------------")

        for topic, data in memory["topics"].items():

            attempted = data["attempted"]
            correct = data["correct"]

            accuracy = (
                correct
                / attempted
                * 100
            )

            print(
                f"{topic}: "
                f"{correct}/{attempted} "
                f"({round(accuracy, 2)}%)"
            )


def get_weak_topic():

    memory = load_memory()

    if not memory["topics"]:
        return None

    weakest_topic = None
    lowest_accuracy = 101

    for topic, data in memory["topics"].items():

        if data["attempted"] == 0:
            continue

        accuracy = (
            data["correct"]
            / data["attempted"]
            * 100
        )

        if accuracy < lowest_accuracy:

            lowest_accuracy = accuracy
            weakest_topic = topic

    return weakest_topic
import json
import os


MEMORY_FILE = "progress.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):

        return {
            "total": 0,
            "correct": 0,
            "wrong": 0
        }

    try:

        with open(MEMORY_FILE, "r") as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return {
            "total": 0,
            "correct": 0,
            "wrong": 0
        }


def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:

        json.dump(
            memory,
            file,
            indent=4
        )


def record_result(is_correct):

    memory = load_memory()

    memory["total"] += 1

    if is_correct:

        memory["correct"] += 1

    else:

        memory["wrong"] += 1

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
            "Accuracy:",
            round(accuracy, 2),
            "%"
        )
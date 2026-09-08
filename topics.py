TOPICS = {
    "Percentage": {
        "types": [
            "PERCENTAGE",
            "DISCOUNT",
            "INCREASE"
        ]
    },

    "Profit and Loss": {
        "types": [
            "PROFIT",
            "LOSS"
        ]
    },

    "Ratio and Proportion": {
        "types": [
            "RATIO"
        ]
    },

    "Average": {
        "types": [
            "AVERAGE"
        ]
    },

    "Simple Interest": {
        "types": [
            "SIMPLE_INTEREST"
        ]
    },

    "Time and Work": {
        "types": [
            "TIME_WORK"
        ]
    },

    "Time Speed and Distance": {
        "types": [
            "SPEED",
            "DISTANCE",
            "TIME"
        ]
    },

    "Number System": {
        "types": [
            "NUMBER_SYSTEM"
        ]
    }
}


def get_available_topics():
    return list(TOPICS.keys())


def get_topic_types(topic):
    return TOPICS.get(topic, {}).get("types", [])
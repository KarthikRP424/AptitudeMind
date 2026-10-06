"""
AptitudeMind - Question Adapter
"""

import re


def adapt_profit_percentage(question):
    if not isinstance(question, dict):
        return {"status": "error", "message": "Question must be a dictionary."}

    question_text = question.get("question")
    if not question_text:
        return {"status": "error", "message": "Question text is missing."}

    cost_match = re.search(
        r"bought\s+for\s+₹?\s*(\d+(?:\.\d+)?)",
        question_text,
        re.IGNORECASE
    )
    selling_match = re.search(
        r"sold\s+for\s+₹?\s*(\d+(?:\.\d+)?)",
        question_text,
        re.IGNORECASE
    )

    if not cost_match or not selling_match:
        return {
            "status": "error",
            "message": "Could not extract cost price and selling price."
        }

    cost_price = float(cost_match.group(1))
    selling_price = float(selling_match.group(1))

    if cost_price <= 0 or selling_price <= 0:
        return {
            "status": "error",
            "message": "Cost price and selling price must be greater than zero."
        }

    if cost_price.is_integer():
        cost_price = int(cost_price)
    if selling_price.is_integer():
        selling_price = int(selling_price)

    return {
        "status": "success",
        "question": {
            "question": question_text,
            "topic": "Profit and Loss",
            "type": "PROFIT_PERCENTAGE",
            "difficulty": question.get("difficulty"),
            "company": question.get("company"),
            "source": question.get("source"),
            "parameters": {
                "cost_price": cost_price,
                "selling_price": selling_price
            },
            "options": ["10", "15", "20", "25"]
        },
        "message": "Question successfully adapted."
    }


def adapt_profit(question):
    if not isinstance(question, dict):
        return {"status": "error", "message": "Question must be a dictionary."}

    question_text = question.get("question")
    if not question_text:
        return {"status": "error", "message": "Question text is missing."}

    cost_match = re.search(
        r"buys\s+an\s+article\s+for\s+₹?\s*(\d+(?:\.\d+)?)",
        question_text,
        re.IGNORECASE
    )
    profit_match = re.search(
        r"profit\s+of\s+(\d+(?:\.\d+)?)\s*%",
        question_text,
        re.IGNORECASE
    )

    if not cost_match or not profit_match:
        return {
            "status": "error",
            "message": "Could not extract cost price and profit percentage."
        }

    cost_price = float(cost_match.group(1))
    profit_percentage = float(profit_match.group(1))

    if cost_price <= 0:
        return {
            "status": "error",
            "message": "Cost price must be greater than zero."
        }

    if profit_percentage <= 0:
        return {
            "status": "error",
            "message": "Profit percentage must be greater than zero."
        }

    if cost_price.is_integer():
        cost_price = int(cost_price)
    if profit_percentage.is_integer():
        profit_percentage = int(profit_percentage)

    return {
        "status": "success",
        "question": {
            "question": question_text,
            "topic": "Profit and Loss",
            "type": "PROFIT",
            "difficulty": question.get("difficulty"),
            "company": question.get("company"),
            "source": question.get("source"),
            "parameters": {
                "cost_price": cost_price,
                "profit_percentage": profit_percentage
            },
            "options": ["1320", "1350", "1380", "1400"]
        },
        "message": "Question successfully adapted."
    }


def adapt_loss(question):
    """
    Adapt the current Question Bank LOSS question.

    This is a reverse-loss question:
    selling price is known and cost price must be found.
    """

    if not isinstance(question, dict):
        return {"status": "error", "message": "Question must be a dictionary."}

    question_text = question.get("question")
    if not question_text:
        return {"status": "error", "message": "Question text is missing."}

    loss_match = re.search(
        r"(\d+(?:\.\d+)?)\s*%\s*loss",
        question_text,
        re.IGNORECASE
    )
    selling_match = re.search(
        r"selling\s+price\s+is\s+₹?\s*(\d+(?:\.\d+)?)",
        question_text,
        re.IGNORECASE
    )

    if not loss_match or not selling_match:
        return {
            "status": "error",
            "message": (
                "Could not extract loss percentage and selling price."
            )
        }

    loss_percentage = float(loss_match.group(1))
    selling_price = float(selling_match.group(1))

    if loss_percentage <= 0 or loss_percentage >= 100:
        return {
            "status": "error",
            "message": (
                "Loss percentage must be greater than 0 "
                "and less than 100."
            )
        }

    if selling_price <= 0:
        return {
            "status": "error",
            "message": "Selling price must be greater than zero."
        }

    if loss_percentage.is_integer():
        loss_percentage = int(loss_percentage)
    if selling_price.is_integer():
        selling_price = int(selling_price)

    return {
        "status": "success",
        "question": {
            "question": question_text,
            "topic": "Profit and Loss",
            "type": "LOSS",
            "difficulty": question.get("difficulty"),
            "company": question.get("company"),
            "source": question.get("source"),
            "parameters": {
                "selling_price": selling_price,
                "loss_percentage": loss_percentage
            },
            "options": ["800", "1000", "1200", "1250"]
        },
        "message": "Question successfully adapted."
    }


# ============================================================
# Probability Adapters
# ============================================================

def adapt_basic_probability(question):
    """
    Adapt a basic probability question.

    Current supported question-bank example:

        A fair coin is tossed once.
        What is the probability of getting heads?

    Standardized representation:

        favorable outcomes = 1
        total outcomes = 2
    """

    if not isinstance(question, dict):
        return {
            "status": "error",
            "message": "Question must be a dictionary."
        }

    question_text = question.get("question")

    if not question_text:
        return {
            "status": "error",
            "message": "Question text is missing."
        }

    return {
        "status": "success",
        "question": {
            "question": question_text,
            "topic": "Probability",
            "type": "BASIC_PROBABILITY",
            "difficulty": question.get("difficulty"),
            "company": question.get("company"),
            "source": question.get("source"),
            "parameters": {
                "favorable_outcomes": 1,
                "total_outcomes": 2
            },
            "options": ["0.25", "0.5", "0.75", "1"]
        },
        "message": "Question successfully adapted."
    }


def adapt_dice_probability(question):
    """
    Adapt the current Question Bank DICE_PROBABILITY question.

    Current supported question-bank example:

        A die is rolled once.
        What is the probability of getting an even number?

    Favorable outcomes = 2, 4, 6 -> 3
    Total outcomes = 1, 2, 3, 4, 5, 6 -> 6
    """

    if not isinstance(question, dict):
        return {
            "status": "error",
            "message": "Question must be a dictionary."
        }

    question_text = question.get("question")

    if not question_text:
        return {
            "status": "error",
            "message": "Question text is missing."
        }

    return {
        "status": "success",
        "question": {
            "question": question_text,
            "topic": "Probability",
            "type": "DICE_PROBABILITY",
            "difficulty": question.get("difficulty"),
            "company": question.get("company"),
            "source": question.get("source"),
            "parameters": {
                "favorable_outcomes": 3,
                "total_outcomes": 6
            },
            "options": ["0.25", "0.5", "0.6667", "0.75"]
        },
        "message": "Question successfully adapted."
    }


def adapt_question(question):
    if not isinstance(question, dict):
        return {
            "status": "error",
            "message": "Question must be a dictionary."
        }

    question_type = str(
        question.get("type", "")
    ).upper()

    if question_type == "PROFIT_PERCENTAGE":
        return adapt_profit_percentage(question)

    if question_type == "PROFIT":
        return adapt_profit(question)

    if question_type == "LOSS":
        return adapt_loss(question)

    if question_type == "BASIC_PROBABILITY":
        return adapt_basic_probability(question)

    if question_type == "DICE_PROBABILITY":
        return adapt_dice_probability(question)

    return {
        "status": "unsupported",
        "message": (
            f"No adapter exists yet for question type "
            f"'{question_type}'."
        )
    }


# ============================================================
# Tests
# ============================================================

def run_tests():
    print("\n🧪 Question Adapter Tests")
    print("=" * 60)

    # --------------------------------------------------------
    # Test 1 - Profit Percentage
    # --------------------------------------------------------

    profit_percentage_question = {
        "question": (
            "An article is bought for ₹500 and sold for ₹600. "
            "What is the profit percentage?"
        ),
        "section": "Quantitative Aptitude",
        "topic": "Profit and Loss",
        "type": "PROFIT_PERCENTAGE",
        "difficulty": "Easy",
        "company": "Infosys",
        "source": "company_style",
        "answer": 20
    }

    result = adapt_question(profit_percentage_question)

    print("\nTest 1 - PROFIT_PERCENTAGE")
    print(result)

    assert result["status"] == "success"

    assert result["question"]["parameters"] == {
        "cost_price": 500,
        "selling_price": 600
    }

    assert result["question"]["options"] == [
        "10",
        "15",
        "20",
        "25"
    ]

    print("✅ PROFIT_PERCENTAGE adapter test passed.")

    # --------------------------------------------------------
    # Test 2 - Profit
    # --------------------------------------------------------

    profit_question = {
        "question": (
            "A shopkeeper buys an article for ₹1200 and sells it "
            "at a profit of 15%. Find the selling price."
        ),
        "section": "Quantitative Aptitude",
        "topic": "Profit and Loss",
        "type": "PROFIT",
        "difficulty": "Medium",
        "company": "Infosys",
        "source": "company_style",
        "answer": 1380
    }

    result = adapt_question(profit_question)

    print("\nTest 2 - PROFIT")
    print(result)

    assert result["status"] == "success"

    assert result["question"]["parameters"] == {
        "cost_price": 1200,
        "profit_percentage": 15
    }

    assert result["question"]["options"] == [
        "1320",
        "1350",
        "1380",
        "1400"
    ]

    print("✅ PROFIT adapter test passed.")

    # --------------------------------------------------------
    # Test 3 - Loss
    # --------------------------------------------------------

    loss_question = {
        "question": (
            "An article is sold at a 20% loss. If the selling "
            "price is ₹960, what was its cost price?"
        ),
        "section": "Quantitative Aptitude",
        "topic": "Profit and Loss",
        "type": "LOSS",
        "difficulty": "Hard",
        "company": "Infosys",
        "source": "company_style",
        "answer": 1200
    }

    result = adapt_question(loss_question)

    print("\nTest 3 - LOSS")
    print(result)

    assert result["status"] == "success"

    assert result["question"]["parameters"] == {
        "selling_price": 960,
        "loss_percentage": 20
    }

    assert result["question"]["options"] == [
        "800",
        "1000",
        "1200",
        "1250"
    ]

    print("✅ LOSS adapter test passed.")

    # --------------------------------------------------------
    # Test 4 - Basic Probability
    # --------------------------------------------------------

    basic_probability_question = {
        "question": (
            "A fair coin is tossed once. "
            "What is the probability of getting heads?"
        ),
        "section": "Quantitative Aptitude",
        "topic": "Probability",
        "type": "BASIC_PROBABILITY",
        "difficulty": "Easy",
        "company": "Amazon",
        "source": "company_style",
        "answer": 0.5
    }

    result = adapt_question(basic_probability_question)

    print("\nTest 4 - BASIC_PROBABILITY")
    print(result)

    assert result["status"] == "success"

    assert result["question"]["type"] == "BASIC_PROBABILITY"

    assert result["question"]["parameters"] == {
        "favorable_outcomes": 1,
        "total_outcomes": 2
    }

    assert result["question"]["options"] == [
        "0.25",
        "0.5",
        "0.75",
        "1"
    ]

    print("✅ BASIC_PROBABILITY adapter test passed.")

    # --------------------------------------------------------
    # Test 5 - Dice Probability
    # --------------------------------------------------------

    dice_probability_question = {
        "question": (
            "A die is rolled once. "
            "What is the probability of getting an even number?"
        ),
        "section": "Quantitative Aptitude",
        "topic": "Probability",
        "type": "DICE_PROBABILITY",
        "difficulty": "Medium",
        "company": "Amazon",
        "source": "company_style",
        "answer": 0.5
    }

    result = adapt_question(dice_probability_question)

    print("\nTest 5 - DICE_PROBABILITY")
    print(result)

    assert result["status"] == "success"

    assert result["question"]["type"] == "DICE_PROBABILITY"

    assert result["question"]["parameters"] == {
        "favorable_outcomes": 3,
        "total_outcomes": 6
    }

    assert result["question"]["options"] == [
        "0.25",
        "0.5",
        "0.6667",
        "0.75"
    ]

    print("✅ DICE_PROBABILITY adapter test passed.")

    # --------------------------------------------------------
    # Final Result
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("🎉 ALL QUESTION ADAPTER TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
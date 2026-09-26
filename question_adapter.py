"""
AptitudeMind - Question Adapter
"""

import re


def adapt_profit_percentage(question):
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
            "message": (
                "Could not extract cost price and selling price."
            )
        }

    cost_price = float(cost_match.group(1))
    selling_price = float(selling_match.group(1))

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
            "options": [
                "10",
                "15",
                "20",
                "25"
            ]
        },
        "message": "Question successfully adapted."
    }


def adapt_profit(question):
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
            "message": (
                "Could not extract cost price and profit percentage."
            )
        }

    cost_price = float(cost_match.group(1))
    profit_percentage = float(profit_match.group(1))

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
            "options": [
                "1320",
                "1350",
                "1380",
                "1400"
            ]
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

    loss_percentage = float(
        loss_match.group(1)
    )

    selling_price = float(
        selling_match.group(1)
    )

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
            "options": [
                "800",
                "1000",
                "1200",
                "1250"
            ]
        },
        "message": "Question successfully adapted."
    }


def adapt_question(question):
    """
    Adapt a Question Bank question into the
    standard AptitudeMind question format.

    Returns:
        dict
    """

    if not isinstance(question, dict):
        return {
            "status": "error",
            "question": None,
            "message": "Question must be a dictionary."
        }

    question_type = str(
        question.get("type", "")
    ).upper()

    if question_type == "PROFIT_PERCENTAGE":
        return adapt_profit_percentage(
            question
        )

    if question_type == "PROFIT":
        return adapt_profit(
            question
        )

    if question_type == "LOSS":
        return adapt_loss(
            question
        )

    return {
        "status": "unsupported",
        "question": None,
        "message": (
            f"No adapter exists yet for question type "
            f"'{question_type}'."
        )
    }


def run_tests():

    print("\n🧪 Question Adapter Tests")
    print("=" * 60)

    # ========================================================
    # TEST 1 - PROFIT_PERCENTAGE
    # ========================================================

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

    result = adapt_question(
        profit_percentage_question
    )

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

    # ========================================================
    # TEST 2 - PROFIT
    # ========================================================

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

    result = adapt_question(
        profit_question
    )

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

    # ========================================================
    # TEST 3 - LOSS
    # ========================================================

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

    result = adapt_question(
        loss_question
    )

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

    print("\n" + "=" * 60)
    print("🎉 ALL QUESTION ADAPTER TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
"""
AptitudeMind - Question Adapter

Responsibilities:
1. Convert legacy Question Bank questions into the
   standardized AptitudeMind question format.
2. Preserve existing Profit / Loss adapters.
3. Prepare Percentage questions for the Answer Engine.
"""


import re


# ============================================================
# PERCENTAGE
# ============================================================

def adapt_percentage(question):
    """
    Adapt a legacy Percentage question.

    Current supported form:

        A number is increased by 20%.
        What is the percentage increase?

    The mathematical meaning is:

        20% of 100 = 20

    Therefore the Answer Engine can deterministically
    calculate the answer using:

        value = 100
        percentage = 20
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

    # --------------------------------------------------------
    # Extract percentage from the question
    # --------------------------------------------------------

    percentage_match = re.search(
        r"(\d+(?:\.\d+)?)\s*%",
        question_text
    )

    if not percentage_match:

        return {
            "status": "error",
            "message": (
                "Could not extract percentage "
                "from Percentage question."
            )
        }

    percentage = float(
        percentage_match.group(1)
    )

    if percentage < 0:

        return {
            "status": "error",
            "message": "Percentage cannot be negative."
        }

    if percentage.is_integer():

        percentage = int(percentage)

    # --------------------------------------------------------
    # Standardized representation
    # --------------------------------------------------------
    #
    # We use 100 as the reference value because the question
    # asks for the percentage increase itself.
    #
    # Example:
    #
    # 20% of 100 = 20
    #
    # This allows the deterministic Answer Engine to verify
    # the result.
    # --------------------------------------------------------

    return {
        "status": "success",
        "question": {

            "question": question_text,

            "topic": "Percentage",

            "type": "PERCENTAGE",

            "difficulty": question.get(
                "difficulty"
            ),

            "company": question.get(
                "company"
            ),

            "source": question.get(
                "source"
            ),

            "parameters": {

                "value": 100,

                "percentage": percentage

            },

            "options": [
                "10",
                "15",
                "20",
                "25"
            ]

        },

        "message": (
            "Percentage question successfully adapted."
        )
    }


# ============================================================
# PROFIT PERCENTAGE
# ============================================================

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
                "Could not extract cost price "
                "and selling price."
            )
        }

    cost_price = float(
        cost_match.group(1)
    )

    selling_price = float(
        selling_match.group(1)
    )

    if cost_price <= 0:

        return {
            "status": "error",
            "message": "Cost price must be greater than zero."
        }

    if selling_price <= 0:

        return {
            "status": "error",
            "message": "Selling price must be greater than zero."
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

            "difficulty": question.get(
                "difficulty"
            ),

            "company": question.get(
                "company"
            ),

            "source": question.get(
                "source"
            ),

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

        "message": (
            "Question successfully adapted."
        )
    }


# ============================================================
# PROFIT
# ============================================================

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
                "Could not extract cost price "
                "and profit percentage."
            )
        }

    cost_price = float(
        cost_match.group(1)
    )

    profit_percentage = float(
        profit_match.group(1)
    )

    if cost_price <= 0:

        return {
            "status": "error",
            "message": "Cost price must be greater than zero."
        }

    if profit_percentage < 0:

        return {
            "status": "error",
            "message": (
                "Profit percentage cannot be negative."
            )
        }

    if cost_price.is_integer():

        cost_price = int(cost_price)

    if profit_percentage.is_integer():

        profit_percentage = int(
            profit_percentage
        )

    return {
        "status": "success",
        "question": {

            "question": question_text,

            "topic": "Profit and Loss",

            "type": "PROFIT",

            "difficulty": question.get(
                "difficulty"
            ),

            "company": question.get(
                "company"
            ),

            "source": question.get(
                "source"
            ),

            "parameters": {

                "cost_price": cost_price,

                "profit_percentage":
                    profit_percentage

            },

            "options": [
                "1320",
                "1350",
                "1380",
                "1400"
            ]

        },

        "message": (
            "Question successfully adapted."
        )
    }


# ============================================================
# LOSS
# ============================================================

def adapt_loss(question):
    """
    Adapt the current Question Bank LOSS question.

    This is a reverse-loss question:

        Selling price is known.
        Cost price must be found.
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
                "Could not extract loss percentage "
                "and selling price."
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
            "message": (
                "Selling price must be greater than zero."
            )
        }

    if loss_percentage.is_integer():

        loss_percentage = int(
            loss_percentage
        )

    if selling_price.is_integer():

        selling_price = int(
            selling_price
        )

    return {
        "status": "success",
        "question": {

            "question": question_text,

            "topic": "Profit and Loss",

            "type": "LOSS",

            "difficulty": question.get(
                "difficulty"
            ),

            "company": question.get(
                "company"
            ),

            "source": question.get(
                "source"
            ),

            "parameters": {

                "selling_price": selling_price,

                "loss_percentage":
                    loss_percentage

            },

            "options": [
                "800",
                "1000",
                "1200",
                "1250"
            ]

        },

        "message": (
            "Question successfully adapted."
        )
    }


# ============================================================
# MAIN ADAPTER ROUTER
# ============================================================

def adapt_question(question):

    if not isinstance(question, dict):

        return {
            "status": "error",
            "message": "Question must be a dictionary."
        }

    question_type = str(
        question.get(
            "type",
            ""
        )
    ).upper()

    # --------------------------------------------------------
    # Percentage
    # --------------------------------------------------------

    if question_type == "PERCENTAGE":

        return adapt_percentage(
            question
        )

    # --------------------------------------------------------
    # Profit Percentage
    # --------------------------------------------------------

    if question_type == "PROFIT_PERCENTAGE":

        return adapt_profit_percentage(
            question
        )

    # --------------------------------------------------------
    # Profit
    # --------------------------------------------------------

    if question_type == "PROFIT":

        return adapt_profit(
            question
        )

    # --------------------------------------------------------
    # Loss
    # --------------------------------------------------------

    if question_type == "LOSS":

        return adapt_loss(
            question
        )

    return {
        "status": "unsupported",
        "message": (
            f"No adapter exists yet for question "
            f"type '{question_type}'."
        )
    }


# ============================================================
# TESTS
# ============================================================

def run_tests():

    print(
        "\n🧪 Question Adapter Tests"
    )

    print(
        "=" * 60
    )

    # ========================================================
    # Test 1 - Percentage
    # ========================================================

    percentage_question = {

        "question": (
            "A number is increased by 20%. "
            "What is the percentage increase?"
        ),

        "section": "Quantitative Aptitude",

        "topic": "Percentage",

        "type": "PERCENTAGE",

        "difficulty": "Easy",

        "company": "TCS",

        "source": "company_style",

        "answer": 20
    }

    result = adapt_question(
        percentage_question
    )

    print(
        "\nTest 1 - PERCENTAGE"
    )

    print(result)

    assert result["status"] == "success"

    assert result["question"]["topic"] == "Percentage"

    assert result["question"]["type"] == "PERCENTAGE"

    assert result["question"]["parameters"] == {
        "value": 100,
        "percentage": 20
    }

    assert result["question"]["options"] == [
        "10",
        "15",
        "20",
        "25"
    ]

    print(
        "✅ PERCENTAGE adapter test passed."
    )

    # ========================================================
    # Test 2 - Profit Percentage
    # ========================================================

    profit_percentage_question = {

        "question": (
            "An article is bought for ₹500 "
            "and sold for ₹600. "
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

    print(
        "\nTest 2 - PROFIT_PERCENTAGE"
    )

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

    print(
        "✅ PROFIT_PERCENTAGE adapter test passed."
    )

    # ========================================================
    # Test 3 - Profit
    # ========================================================

    profit_question = {

        "question": (
            "A shopkeeper buys an article for ₹1200 "
            "and sells it at a profit of 15%. "
            "Find the selling price."
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

    print(
        "\nTest 3 - PROFIT"
    )

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

    print(
        "✅ PROFIT adapter test passed."
    )

    # ========================================================
    # Test 4 - Loss
    # ========================================================

    loss_question = {

        "question": (
            "An article is sold at a 20% loss. "
            "If the selling price is ₹960, "
            "what was its cost price?"
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

    print(
        "\nTest 4 - LOSS"
    )

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

    print(
        "✅ LOSS adapter test passed."
    )

    # ========================================================
    # Final
    # ========================================================

    print(
        "\n" + "=" * 60
    )

    print(
        "🎉 ALL QUESTION ADAPTER TESTS PASSED"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":

    run_tests()
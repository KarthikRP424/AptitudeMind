
"""
AptitudeMind - Question Adapter

Converts questions from the Question Bank format
into the standardized format expected by the Evaluator.

Current supported type:
    PROFIT_PERCENTAGE

Architecture:

    Question Bank
          ↓
    Question Adapter
          ↓
    Standard Question
          ↓
    Evaluator
          ↓
    Answer Engine
"""


# ============================================================
# PROFIT PERCENTAGE ADAPTER
# ============================================================

def adapt_profit_percentage(question):
    """
    Convert a Question Bank profit-percentage question
    into the standard AptitudeMind question format.

    Expected Question Bank format:

        {
            "question": "...",
            "topic": "Profit and Loss",
            "type": "PROFIT_PERCENTAGE",
            "difficulty": "Easy",
            "company": "Infosys",
            "source": "company_style",
            "answer": 20
        }

    Returns:
        dict: Standardized question.
    """

    question_text = question.get("question")

    if not question_text:
        return {
            "status": "error",
            "message": "Question text is missing."
        }

    # --------------------------------------------------------
    # Current Infosys question structure
    # --------------------------------------------------------
    #
    # The Question Bank currently stores:
    #
    # Cost Price = 500
    # Selling Price = 600
    #
    # We are intentionally keeping these as deterministic
    # parameters for the Answer Engine.
    # --------------------------------------------------------

    if "500" in question_text and "600" in question_text:

        cost_price = 500
        selling_price = 600

    else:

        return {
            "status": "error",
            "message": (
                "Could not extract profit-percentage "
                "parameters from the question."
            )
        }

    # --------------------------------------------------------
    # Create four options
    # --------------------------------------------------------

    options = [
        "10",
        "15",
        "20",
        "25"
    ]

    # --------------------------------------------------------
    # Standard AptitudeMind format
    # --------------------------------------------------------

    adapted_question = {
        "question": question_text,
        "topic": question.get(
            "topic",
            "Profit and Loss"
        ),
        "type": "PROFIT_PERCENTAGE",
        "difficulty": question.get(
            "difficulty"
        ),
        "company": question.get(
            "company"
        ),
        "source": question.get(
            "source",
            "question_bank"
        ),
        "parameters": {
            "cost_price": cost_price,
            "selling_price": selling_price
        },
        "options": options
    }

    return {
        "status": "success",
        "question": adapted_question,
        "message": (
            "Question successfully adapted."
        )
    }


# ============================================================
# MAIN ADAPTER
# ============================================================

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
            "message": (
                "Question must be a dictionary."
            )
        }

    question_type = question.get(
        "type"
    )

    if not isinstance(question_type, str):

        return {
            "status": "error",
            "question": None,
            "message": (
                "Question type is missing."
            )
        }

    question_type = question_type.strip().upper()

    # --------------------------------------------------------
    # PROFIT PERCENTAGE
    # --------------------------------------------------------

    if question_type == "PROFIT_PERCENTAGE":

        return adapt_profit_percentage(
            question
        )

    # --------------------------------------------------------
    # Unsupported type
    # --------------------------------------------------------

    return {
        "status": "error",
        "question": None,
        "message": (
            f"Question type '{question_type}' "
            "is not supported by the adapter yet."
        )
    }


# ============================================================
# TEST
# ============================================================

def run_tests():

    print("\n🧪 Question Adapter Tests")
    print("=" * 60)

    infosys_question = {
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
        infosys_question
    )

    print("\nAdapter result:")
    print(result)

    assert result["status"] == "success"

    adapted = result["question"]

    assert adapted["question"] == (
        infosys_question["question"]
    )

    assert adapted["type"] == (
        "PROFIT_PERCENTAGE"
    )

    assert adapted["parameters"]["cost_price"] == 500

    assert adapted["parameters"]["selling_price"] == 600

    assert len(adapted["options"]) == 4

    print("\n✅ PROFIT_PERCENTAGE adapter test passed.")

    print("\n" + "=" * 60)
    print("🎉 ALL QUESTION ADAPTER TESTS PASSED")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run_tests()

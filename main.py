import ollama

from calculator import (
    calculate_percentage,
    calculate_discount,
    calculate_increase
)

from progress import record_result, show_progress


def main():

    print("🤖 AptitudeMind is starting...\n")

    # ---------------------------------------
    # Prompt for Llama
    # ---------------------------------------

    prompt = """
You are AptitudeMind, an intelligent aptitude mentor.

Generate ONE easy-level percentage aptitude question.

Return the result EXACTLY in this format:

QUESTION: <question>
TYPE: <type>
VALUE: <number>
PERCENTAGE: <number>

TYPE must be exactly ONE of:

PERCENTAGE
DISCOUNT
INCREASE

---------------------------------------
PERCENTAGE QUESTION
---------------------------------------

Ask for the percentage amount itself.

Example:

QUESTION: What is 25% of $200?
TYPE: PERCENTAGE
VALUE: 200
PERCENTAGE: 25

The answer is:

200 × 25 / 100 = 50

---------------------------------------
DISCOUNT QUESTION
---------------------------------------

Ask for the final price after a percentage discount.

Example:

QUESTION: A shirt costs $200 and is available at 25% off. What is the final price?
TYPE: DISCOUNT
VALUE: 200
PERCENTAGE: 25

The answer is:

200 - (200 × 25 / 100) = 150

---------------------------------------
INCREASE QUESTION
---------------------------------------

Ask for the final value after a percentage increase.

Example:

QUESTION: A salary is $200 and increases by 25%. What is the new salary?
TYPE: INCREASE
VALUE: 200
PERCENTAGE: 25

The answer is:

200 + (200 × 25 / 100) = 250

---------------------------------------
STRICT RULES
---------------------------------------

1. Generate exactly ONE question.

2. The question must contain all necessary numerical information.

3. VALUE must appear meaningfully in the question.

4. PERCENTAGE must appear meaningfully in the question.

5. The question must have exactly ONE clear numerical answer.

6. The question must be completely self-contained.

7. TYPE must correctly describe the mathematical operation.

8. Do not generate ambiguous questions.

9. Do not generate exam-score or marks questions.

10. Do not mix discount and percentage calculations.

11. Do not mix increase and percentage calculations.

12. For DISCOUNT questions, ask for the final price after discount.

13. For INCREASE questions, ask for the final value after increase.

14. For PERCENTAGE questions, ask for the percentage amount.

15. Do not give the answer.

16. Do not give a solution.

17. Do not include explanations.

18. Do not include any extra text.
"""

    # ---------------------------------------
    # Ask Llama to generate question
    # ---------------------------------------

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response["message"]["content"]

    # ---------------------------------------
    # Extract structured information
    # ---------------------------------------

    lines = result.strip().split("\n")

    question = ""
    question_type = ""
    value = ""
    percentage = ""

    for line in lines:

        if line.startswith("QUESTION:"):
            question = line.replace(
                "QUESTION:",
                ""
            ).strip()

        elif line.startswith("TYPE:"):
            question_type = line.replace(
                "TYPE:",
                ""
            ).strip().upper()

        elif line.startswith("VALUE:"):
            value = line.replace(
                "VALUE:",
                ""
            ).strip()

        elif line.startswith("PERCENTAGE:"):
            percentage = line.replace(
                "PERCENTAGE:",
                ""
            ).strip()

    # ---------------------------------------
    # Check generated question
    # ---------------------------------------

    if not question:
        print("\n⚠️ AptitudeMind could not generate a question.")
        return

    if not question_type:
        print("\n⚠️ Question type is missing.")
        return

    # ---------------------------------------
    # Show ONLY the question
    # ---------------------------------------

    print("🧠 AptitudeMind:")
    print("\n📚 Question:", question)

    # ---------------------------------------
    # Convert VALUE and PERCENTAGE
    # ---------------------------------------

    try:

        value = float(value)
        percentage = float(percentage)

    except ValueError:

        print("\n⚠️ AptitudeMind could not process the question.")
        return

    # ---------------------------------------
    # Choose calculator based on TYPE
    # ---------------------------------------

    if question_type == "PERCENTAGE":

        correct_answer = calculate_percentage(
            value,
            percentage
        )

    elif question_type == "DISCOUNT":

        correct_answer = calculate_discount(
            value,
            percentage
        )

    elif question_type == "INCREASE":

        correct_answer = calculate_increase(
            value,
            percentage
        )

    else:

        print("\n⚠️ Unknown question type:", question_type)
        return

    # ---------------------------------------
    # Ask student for answer
    # ---------------------------------------

    student_answer = input(
        "\n👨‍🎓 Your answer: "
    )

    # ---------------------------------------
    # Evaluate student answer
    # ---------------------------------------

    try:

        student_value = float(student_answer)

        # Allow tiny decimal differences
        if abs(student_value - correct_answer) < 0.01:

            print("\n✅ Correct! Excellent work! 🔥")
            print("🧠 You calculated the answer correctly.")

            record_result(True)

        else:

            print("\n❌ Incorrect.")
            print(
                "💡 Correct answer:",
                correct_answer
            )

            record_result(False)

            # ---------------------------------------
            # Explanation
            # ---------------------------------------

            print("\n📖 Let's understand:")

            if question_type == "PERCENTAGE":

                print(
                    f"{percentage}% of {value}"
                )

                print(
                    f"= {value} × {percentage} / 100"
                )

                print(
                    f"= {correct_answer}"
                )

            elif question_type == "DISCOUNT":

                discount = calculate_percentage(
                    value,
                    percentage
                )

                print(
                    f"Discount = {percentage}% of {value}"
                )

                print(
                    f"= {value} × {percentage} / 100"
                )

                print(
                    f"= {discount}"
                )

                print("\nFinal price:")

                print(
                    f"= {value} - {discount}"
                )

                print(
                    f"= {correct_answer}"
                )

            elif question_type == "INCREASE":

                increase = calculate_percentage(
                    value,
                    percentage
                )

                print(
                    f"Increase = {percentage}% of {value}"
                )

                print(
                    f"= {value} × {percentage} / 100"
                )

                print(
                    f"= {increase}"
                )

                print("\nNew value:")

                print(
                    f"= {value} + {increase}"
                )

                print(
                    f"= {correct_answer}"
                )

    except ValueError:

        print(
            "\n⚠️ Please enter a valid numerical answer."
        )

    # ---------------------------------------
    # Show progress
    # ---------------------------------------

    show_progress()


if __name__ == "__main__":
    main()
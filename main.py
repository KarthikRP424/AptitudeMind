import ollama
from calculator import calculate_percentage


def main():
    print("🤖 AptitudeMind is starting...\n")

    prompt = """
You are AptitudeMind, an intelligent aptitude mentor.

Generate ONE easy-level percentage question.

Return the result EXACTLY in this format:

QUESTION: <question>
VALUE: <number>
PERCENTAGE: <number>

STRICT RULES:

1. The question must explicitly contain VALUE.
2. The question must explicitly contain PERCENTAGE.
3. The question must ask something that can be calculated as:
   VALUE × PERCENTAGE / 100
4. VALUE must appear meaningfully in the question.
5. PERCENTAGE must appear meaningfully in the question.
6. The question must have exactly one clear numerical answer.
7. The question must be completely self-contained.
8. Do not generate questions about exam scores, marks, percentages already obtained, or percentage changes.
9. Do not generate an incomplete question.
10. Do not give the answer.
11. Do not include explanations.
12. Do not include any extra text.

GOOD EXAMPLE:

QUESTION: A book costs $15. What is 20% of the cost?
VALUE: 15
PERCENTAGE: 20

BAD EXAMPLE:

QUESTION: A school scored 85% in the recent examination.
VALUE: 85
PERCENTAGE: 5

Never generate a question like the BAD example.
"""

    # Ask Llama to generate the question
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

    # Extract internal information
    lines = result.strip().split("\n")

    question = ""
    value = ""
    percentage = ""

    for line in lines:
        if line.startswith("QUESTION:"):
            question = line.replace("QUESTION:", "").strip()

        elif line.startswith("VALUE:"):
            value = line.replace("VALUE:", "").strip()

        elif line.startswith("PERCENTAGE:"):
            percentage = line.replace("PERCENTAGE:", "").strip()

    # Show ONLY the question to the student
    print("🧠 AptitudeMind:")
    print("\n📚 Question:", question)

    # Calculate the correct answer internally
    try:
        value = float(value)
        percentage = float(percentage)

        correct_answer = calculate_percentage(value, percentage)

    except ValueError:
        print("\n⚠️ AptitudeMind could not process the question.")
        return

    # Ask the student for their answer
    student_answer = input("\n👨‍🎓 Your answer: ")

    # Evaluate the student's answer
    try:
        student_value = float(student_answer)

        if student_value == correct_answer:
            print("\n✅ Correct! Excellent work! 🔥")
            print("🧠 You calculated the percentage correctly.")

        else:
            print("\n❌ Incorrect.")
            print("💡 Correct answer:", correct_answer)

            print("\n📖 Let's understand:")
            print(f"{percentage}% of {value}")
            print(f"= {value} × {percentage} / 100")
            print(f"= {correct_answer}")

    except ValueError:
        print("\n⚠️ Please enter a valid numerical answer.")


if __name__ == "__main__":
    main()
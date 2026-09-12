# ============================================================
# AptitudeMind - AI Question Generator
# ============================================================

import ollama


# ============================================================
# Generate Aptitude Question
# ============================================================

def generate_question(topic, difficulty, company=None):

    company_text = company if company else "general placement"

    prompt = f"""
You are an expert aptitude question generator.

Create ONE {difficulty}-level aptitude question.

Topic: {topic}
Company style: {company_text}

Requirements:
1. The question must be clear and unambiguous.
2. It must have exactly one correct numerical or textual answer.
3. Do not provide the answer.
4. Do not provide explanation.
5. Do not create a trick question.
6. Return only the question.

Question:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


# ============================================================
# Test Generator
# ============================================================

if __name__ == "__main__":

    print("🤖 AptitudeMind AI Question Generator")
    print("=====================================")

    question = generate_question(
        topic="Algebra",
        difficulty="Hard",
        company="TCS"
    )

    print("\n📚 Generated Question:")
    print(question)
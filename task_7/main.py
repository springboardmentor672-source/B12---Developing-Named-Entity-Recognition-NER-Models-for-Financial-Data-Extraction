import ollama

MODEL_NAME = "llama3:8b"


def simplify_text(text):
    prompt = f"""
You are a language simplification assistant.

Rewrite the following text in simple and easy-to-understand language.
Do NOT summarize.
Keep all information.
Just simplify wording.

Text:
{text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


def main():
    print("=== Local LLM Text Simplifier (Llama3) ===")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter text:\n")

        if user_input.lower() == "exit":
            break

        simplified = simplify_text(user_input)

        print("\nSimplified Version:\n")
        print(simplified)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
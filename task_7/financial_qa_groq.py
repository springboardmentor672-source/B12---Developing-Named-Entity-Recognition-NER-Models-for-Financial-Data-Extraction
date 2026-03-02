import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_markdown(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
x
def chunk_text(text, max_chars=3000):
    """Split text into smaller chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end
    return chunks


def ask_question(document: str, question: str) -> str:
    chunks = chunk_text(document)

    for chunk in chunks:
        prompt = f"""
You are a financial document assistant.

Below is a PART of a financial document:
------------------------------
{chunk}
------------------------------

Question: {question}

If the answer is not present in this text, say "Not found in this section."
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a finance-aware assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=200
        )

        answer = response.choices[0].message.content.strip()

        if "not found" not in answer.lower():
            return answer

    return "Answer not found in the provided document."


if __name__ == "__main__":
    md_file = "apple_report.md"
    document_text = load_markdown(md_file)

    print("Financial Question Answering Tool (Groq)")
    print("Type 'exit' to quit\n")

    while True:
        question = input("Ask a question: ")
        if question.lower() == "exit":
            break

        answer = ask_question(document_text, question)
        print("\nAnswer:")
        print(answer)
        print("-" * 80)
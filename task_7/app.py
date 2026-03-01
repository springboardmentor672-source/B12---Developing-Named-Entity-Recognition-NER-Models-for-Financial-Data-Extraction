import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found in .env file")
    exit()

client = Groq(api_key=api_key)


def analyze_spending(expense_text):

    prompt = f"""
You are a financial assistant.

Analyze the following expense data.

Tasks:
1. Categorize each expense (Food, Shopping, Transport, Subscription, etc.)
2. Calculate total spending
3. Identify highest spending category
4. Give 3 short savings suggestions

Return output ONLY in JSON format like this:

{{
  "total_spent": number,
  "categories": {{
      "Food": number,
      "Shopping": number
  }},
  "highest_spending_category": "category_name",
  "suggestions": ["suggestion1", "suggestion2", "suggestion3"]
}}

Expense Data:
{expense_text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # Stable working model
            messages=[
                {"role": "system", "content": "You are a financial behavior analyzer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ API Error:", e)
        return None


def main():
    print("\n💳 Daily Spending Behavior Analyzer")
    print("-" * 45)
    print("Enter your expenses (Press Enter twice to finish):\n")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    expense_text = "\n".join(lines)

    if not expense_text.strip():
        print("❌ No input provided.")
        return

    print("\n⏳ Analyzing...\n")

    result = analyze_spending(expense_text)

    if not result:
        return

    try:
        # 🔥 Clean markdown JSON if model adds ```json
        clean_result = result.strip()

        if clean_result.startswith("```"):
            clean_result = clean_result.replace("```json", "")
            clean_result = clean_result.replace("```", "")
            clean_result = clean_result.strip()

        data = json.loads(clean_result)

        print("📊 Spending Report")
        print("-" * 45)
        print(f"Total Spent: ₹{data['total_spent']}")

        print("\nCategory Breakdown:")
        for category, amount in data["categories"].items():
            print(f"• {category}: ₹{amount}")

        print(f"\nHighest Spending: {data['highest_spending_category']}")

        print("\n💡 Suggestions:")
        for s in data["suggestions"]:
            print(f"• {s}")

        print("-" * 45)

    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON. Raw Output:\n")
        print(result)


if __name__ == "__main__":
    main()
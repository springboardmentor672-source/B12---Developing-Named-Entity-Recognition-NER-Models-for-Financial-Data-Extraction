import os
import langextract as lx
from dotenv import load_dotenv
from langextract.providers.openai import OpenAILanguageModel

load_dotenv()

# ---------------- MODEL SETUP ----------------
groq_model = OpenAILanguageModel(
    model_id="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# ---------------- PROMPT (IMPROVED) ----------------
PROMPT = """
Extract financial entities from the text.

Return ONLY valid values (no nulls).

Extract:
- company (e.g., Apple, Tesla)
- money (e.g., $100 billion, ₹500 crore)
- percentage (e.g., 10%, 5.6%)
- date (e.g., 2023, June 2025)
- product (e.g., iPhone, MacBook)
- metric (e.g., revenue, net income, profit)
"""

# ---------------- EXAMPLES ----------------
EXAMPLES = [
    lx.data.ExampleData(
        text="Apple earned $100 billion in 2023.",
        extractions=[
            lx.data.Extraction("company", "Apple"),
            lx.data.Extraction("money", "$100 billion"),
            lx.data.Extraction("date", "2023"),
        ],
    )
]

# ---------------- MAIN FUNCTION ----------------
def extract_finance_entities(text: str):
    try:
        result = lx.extract(
            text_or_documents=text[:20000],
            prompt_description=PROMPT,
            examples=EXAMPLES,
            model=groq_model
        )

        output = []

        for e in result.extractions:
            # ✅ FIX 1: Skip None values
            if e.extraction_text is None:
                continue

            # ✅ FIX 2: Convert safely to string
            cleaned_text = str(e.extraction_text).strip()

            # ✅ FIX 3: Skip empty strings
            if cleaned_text == "":
                continue

            output.append({
                "type": e.extraction_class,
                "text": cleaned_text
            })

        return output

    except Exception as e:
        print("LangExtract Error:", str(e))
        return []
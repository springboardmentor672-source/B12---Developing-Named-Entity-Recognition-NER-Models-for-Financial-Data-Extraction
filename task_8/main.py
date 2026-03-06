import os
import sys
import json
import fitz
import langextract as lx
from dotenv import load_dotenv
from langextract.providers.openai import OpenAILanguageModel


# =====================================
# PHASE 1 — Load Environment
# =====================================
print("🔹 Loading environment variables...")
load_dotenv()

GROQ_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")

if not GROQ_KEY:
    print("❌ OPENAI_API_KEY missing in .env")
    sys.exit(1)

print("✅ API Key Loaded.")


# =====================================
# PHASE 2 — Setup Groq Model
# =====================================
print("🔹 Connecting to Groq Llama 3.3...")

model = OpenAILanguageModel(
    model_id="llama-3.3-70b-versatile",
    api_key=GROQ_KEY,
    base_url=BASE_URL,
    temperature=0.1
)

print("✅ Model Connected.")


# =====================================
# PHASE 3 — PDF → Markdown
# =====================================
def convert_pdf_to_md(pdf_path, output_path="output.md"):

    print("🔹 Converting PDF → Markdown...")

    doc = fitz.open(pdf_path)
    md_text = ""

    for page_num, page in enumerate(doc):
        md_text += f"\n\n# Page {page_num + 1}\n\n"
        md_text += page.get_text()

    doc.close()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    print("✅ Markdown file created:", output_path)
    return output_path


# =====================================
# PHASE 4 — Few-Shot Example (UPDATED)
# =====================================
examples = [
    lx.data.ExampleData(
        text="Tesla reported revenue growth of 25% in FY2023.",
        extractions=[
            lx.data.Extraction("organization", "Tesla"),
            lx.data.Extraction("financial_metric", "revenue"),
            lx.data.Extraction("growth_rate", "25%")
        ]
    )
]

PROMPT = """
You are a financial Named Entity Recognition (NER) system.

Extract the following entities:

1. organization → Company names
2. financial_metric → revenue, profit, net income, EBITDA, operating income, assets, liabilities
3. growth_rate → percentage increase or decrease (e.g., 15%, 10% growth, 8% decline)

Rules:
- Extract exact words from the text
- Do not modify the original wording
- Do not hallucinate entities
- Only return entities found in the document
"""


# =====================================
# PHASE 5 — Main Execution
# =====================================
def main():

    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf_file>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print("❌ PDF file not found!")
        sys.exit(1)

    # Convert PDF
    md_path = convert_pdf_to_md(pdf_path)

    # Read Markdown
    print("🔹 Reading Markdown...")
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    text = text[:4000]  # token safety
    print("✅ Markdown loaded.")

    # Run Extraction
    print("🚀 Running Financial NER...")

    results = lx.extract(
        text,
        PROMPT,
        examples,
        model=model
    )

    print("✅ Extraction Completed.")


    # =====================================
    # PRINT RESULTS
    # =====================================
    print("\n📌 Extracted Entities:")
    print("-" * 40)

    for entity in results.extractions:
        print(f"{entity.extraction_class.upper()} → {entity.extraction_text}")

    print("-" * 40)
    print(f"Total Entities Found: {len(results.extractions)}")


    # =====================================
    # SAVE JSON
    # =====================================
    json_output = [
        {
            "entity_name": e.extraction_class,
            "value": e.extraction_text
        }
        for e in results.extractions
    ]

    with open("finance_entities.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4)

    print("✅ JSON saved as finance_entities.json")


    # =====================================
    # HTML Visualization
    # =====================================
    html_content = lx.visualize(results)
    output_html = html_content.data if hasattr(html_content, "data") else html_content

    with open("finance_visualization.html", "w", encoding="utf-8") as f:
        f.write(output_html)

    print("✅ HTML visualization saved as finance_visualization.html")


if __name__ == "__main__":
    main()
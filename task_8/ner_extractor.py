import os
import json
import langextract as lx
from dotenv import load_dotenv
from langextract.providers.openai import OpenAILanguageModel

# 1. Setup
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

# 2. Setup Model (Llama 3.3)
groq_model = OpenAILanguageModel(
    model_id="llama-3.3-70b-versatile",
    api_key=GROQ_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# 3. Check File
FILE_NAME = "docling.txt"
if not os.path.exists(FILE_NAME):
    print(f"❌ Error: {FILE_NAME} not found!")
    exit()

with open(FILE_NAME, "r", encoding="utf-8") as f:
    # Processing the first 5000 chars gives you the header and the first table
    text_content = f.read()[:5000] 


PROMPT = (
    "Extract financial entities: Company names, Ticker symbols, Dates, "
    "Money amounts, Percentages, and SEC Form types."
)


EXAMPLES = [
    lx.data.ExampleData(
        text="Apple Inc. filed FORM 10-K for fiscal year ended September 28, 2024. AAPL is on Nasdaq.",
        extractions=[
            lx.data.Extraction("company", "Apple Inc."),
            lx.data.Extraction("form_type", "FORM 10-K"),
            lx.data.Extraction("date", "September 28, 2024"),
            lx.data.Extraction("ticker", "AAPL"),
            lx.data.Extraction("exchange", "Nasdaq")
        ]
    ),
    lx.data.ExampleData(
        text="The market value was $2,628,553,000,000 and growth was 0.875%.",
        extractions=[
            lx.data.Extraction("money", "$2,628,553,000,000"),
            lx.data.Extraction("percentage", "0.875%")
        ]
    )
]


print(f"🚀 Processing {FILE_NAME} and generating JSON...")
try:
    results = lx.extract(
        text_or_documents=text_content,
        prompt_description=PROMPT,
        examples=EXAMPLES,
        model=groq_model
    )

    html_content = lx.visualize(results)
    output_html = html_content.data if hasattr(html_content, 'data') else html_content
    with open("finance_visualization.html", "w", encoding="utf-8") as f:
        f.write(output_html)
    

    entities_json = []
    for e in results.extractions:
        entities_json.append({
            "class": e.extraction_class,
            "text": e.extraction_text,
            "start": e.char_interval.start_pos if e.char_interval else None,
            "end": e.char_interval.end_pos if e.char_interval else None,
        })

    with open("finance_entities.json", "w", encoding="utf-8") as f:
        json.dump(entities_json, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Success! Found {len(results.extractions)} entities.")
    print("📁 Files generated: finance_visualization.html & finance_entities.json")

except Exception as e:
    print(f"❌ Error: {e}")
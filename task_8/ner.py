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


FILE_PATH = "apple_report.md"

if not os.path.exists(FILE_PATH):
    print(" Error: apple_report.md not found!")
    exit()

with open(FILE_PATH, "r", encoding="utf-8") as f:
    text_content = f.read()[:30000]

# 4. Simple, Direct Prompt
PROMPT = """
Extract the following entities from the text:

- company: names of companies
- money: monetary values (e.g., $10 billion, USD 5M)
- percentage: percentage values (e.g., 12%, 5.6%)
- date: years, quarters, or fiscal periods
- product: product or service names
- metric: financial metrics such as revenue, net income, gross margin

Return only entities that explicitly appear in the text.
"""


EXAMPLES = [
    lx.data.ExampleData(
        text="Revenue for Microsoft grew by 10% in 2023.",
        extractions=[
            lx.data.Extraction("company", "Microsoft"),
            lx.data.Extraction("metric", "Revenue"),
            lx.data.Extraction("percentage", "10%"),
            lx.data.Extraction("date", "2023"),
        ],
    ),
    lx.data.ExampleData(
        text="Apple reported net income of $94 billion from iPhone sales.",
        extractions=[
            lx.data.Extraction("company", "Apple"),
            lx.data.Extraction("metric", "net income"),
            lx.data.Extraction("money", "$94 billion"),
            lx.data.Extraction("product", "iPhone"),
        ],
    ),
    lx.data.ExampleData(
        text="Amazon invested $5.2 billion in cloud infrastructure during Q4 2022.",
        extractions=[
            lx.data.Extraction("company", "Amazon"),
            lx.data.Extraction("money", "$5.2 billion"),
            lx.data.Extraction("date", "Q4 2022"),
        ],
    ),
]


print(" Extracting characters...")
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
        print(f" Success! Found {len(results.extractions)} entities.")
        print("Right-click 'finance_visualization.html' and 'Open in Browser'.")


except Exception as e:
    print(f" Error: {e}")
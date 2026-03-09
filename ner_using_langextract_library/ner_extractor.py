import os
import json
import langextract as lx
from dotenv import load_dotenv
from langextract.providers.openai import OpenAILanguageModel

# Loading API Key
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    print("Error: GROQ_API_KEY not found in .env file")
    exit()

# Setup Groq Model
groq_model = OpenAILanguageModel(
    model_id="llama-3.3-70b-versatile",
    api_key=GROQ_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Reading Markdown Input File
INPUT_FILE = "input.md"

if not os.path.exists(INPUT_FILE):
    print("Error: input.md not found!")
    exit()

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text_content = f.read()[:3000]   # limit tokens

# Defining Financial NER Prompt
PROMPT = """
Extract financial entities from the given text.

Possible entity types:

- company
- stock_symbol
- revenue
- profit
- loss
- money
- percentage
- date
- person
- product
- market
- currency
- financial_metric

Only extract entities clearly mentioned in the text.
"""

# Few-shot Training Examples

EXAMPLES = [

    lx.data.ExampleData(
        text="Apple reported revenue of $120 billion in Q3 2024.",
        extractions=[
            lx.data.Extraction(extraction_class="company", extraction_text="Apple"),
            lx.data.Extraction(extraction_class="revenue", extraction_text="$120 billion"),
            lx.data.Extraction(extraction_class="date", extraction_text="Q3 2024")
        ]
    ),

    lx.data.ExampleData(
        text="Tesla stock rose by 8% on NASDAQ.",
        extractions=[
            lx.data.Extraction(extraction_class="company", extraction_text="Tesla"),
            lx.data.Extraction(extraction_class="percentage", extraction_text="8%"),
            lx.data.Extraction(extraction_class="market", extraction_text="NASDAQ")
        ]
    ),

    lx.data.ExampleData(
        text="Microsoft CEO Satya Nadella announced new AI products.",
        extractions=[
            lx.data.Extraction(extraction_class="company", extraction_text="Microsoft"),
            lx.data.Extraction(extraction_class="person", extraction_text="Satya Nadella"),
            lx.data.Extraction(extraction_class="product", extraction_text="AI products")
        ]
    ),

    lx.data.ExampleData(
        text="Amazon posted a profit of $30 million in 2023.",
        extractions=[
            lx.data.Extraction(extraction_class="company", extraction_text="Amazon"),
            lx.data.Extraction(extraction_class="profit", extraction_text="$30 million"),
            lx.data.Extraction(extraction_class="date", extraction_text="2023")
        ]
    )
]

print(" Extracting Financial Entities...")


# Running Extraction
try:

    results = lx.extract(
        text_or_documents=text_content,
        prompt_description=PROMPT,
        examples=EXAMPLES,
        model=groq_model
    )

# Generate HTML Visualization
 
    html_content = lx.visualize(results)

    output_html = html_content.data if hasattr(html_content, 'data') else html_content

    with open("finance_visualization.html", "w", encoding="utf-8") as f:
        f.write(output_html)

    # Convert Results to JSON
    entities = []

    for e in results.extractions:
        entities.append({
            "entity": e.extraction_text,
            "type": e.extraction_class
        })

    with open("finance_entities.json", "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=4)

    # Printing Results
    print(f" Success! Found {len(results.extractions)} entities.")
    print(" HTML visualization saved as: finance_visualization.html")
    print(" JSON data saved as: finance_entities.json")


except Exception as e:
    print(f"❌ Error: {e}")
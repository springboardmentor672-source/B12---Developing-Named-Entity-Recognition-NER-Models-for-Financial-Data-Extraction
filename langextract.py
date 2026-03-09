import os
from dotenv import load_dotenv
import langextract as lx
from pypdf import PdfReader
#  Load API Key
load_dotenv()
API_KEY = os.getenv("LANGEXTRACT_API_KEY")
# Read Finance PDF
reader = PdfReader("finance.pdf")
TEXT = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        TEXT += text + "\n"
        TEXT = TEXT[:3500]
# Define Prompt
PROMPT = """
Extract structured financial entities from the text.

Entity classes (STRICTLY USE THESE LABELS):

- organization (companies, institutions, stock exchanges)
- financial_metric (revenue, profit, margin, cash flow)
- percentage (values ending with %)
- currency (monetary values like US$, ₹, crore, million, billion)
- leadership (CEO, Chairman, executives)
- geographic_region (countries, continents, regions)
- esg_metric (carbon neutral, emissions, diversity %)
- regulatory_body (SEBI, IFRS, Companies Act, GRI)

Rules:
1. Percentages MUST be labeled as percentage.
2. Monetary values MUST be labeled as currency.
3. Do not group percentage or currency inside financial_metric.
4. Do not return null values.
"""
#  Example (Improves Accuracy)
EXAMPLES = [
    lx.data.ExampleData(
        text="Apple Inc. reported revenue of $100 billion.",
        extractions=[
            lx.data.Extraction(
                extraction_class="organization",
                extraction_text="Apple Inc.",
                attributes={"type": "company"}
            ),
            lx.data.Extraction(
                extraction_class="financial_metric",
                extraction_text="$100 billion",
                attributes={"metric_type": "revenue"}
            )
        ]
    )
]

#  Run Extraction
result = lx.extract(
    text_or_documents=TEXT,
    prompt_description=PROMPT,
    examples=EXAMPLES,
    api_key=API_KEY,
    max_workers=1   
)
#  Print Output
for extraction in result.extractions:
    print("Class:", extraction.extraction_class)
    print("Text:", extraction.extraction_text)
    print("Attributes:", extraction.attributes)
    print("-" * 40)

# Save Visualization
html_content = lx.visualize(result)

with open("finance_visualization.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Extraction complete!")
print("Visualization saved as finance_visualization.html")
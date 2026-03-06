import os
from dotenv import load_dotenv
import langextract as lx
from pypdf import PdfReader

# -------------------------------
# 1️⃣ Load API Key
# -------------------------------
load_dotenv()
API_KEY = os.getenv("LANGEXTRACT_API_KEY")

# -------------------------------
# 2️⃣ Read Finance PDF
# -------------------------------
reader = PdfReader("finance.pdf")

TEXT = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        TEXT += text + "\n"
        TEXT = TEXT[:4000]

# -------------------------------
# 3️⃣ Define Prompt
# -------------------------------
PROMPT = """
Extract financial entities from the text.

Entity classes:
- organization
- financial_metric
- percentage
- currency
- leadership
- geographic_region
- esg_metric
- stock_symbol
- investment_type
- date
- profit_loss
- market_event
- economic_indicator

For each entity provide:
- extraction_class
- extraction_text
- attributes (if applicable)
"""

# -------------------------------
# 4️⃣ Examples (Few-shot learning)
# -------------------------------
EXAMPLES = [
    lx.data.ExampleData(
        text="Apple Inc. reported revenue of $100 billion in 2023.",
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
            ),
            lx.data.Extraction(
                extraction_class="date",
                extraction_text="2023"
            )
        ]
    ),

    lx.data.ExampleData(
        text="Tesla stock (TSLA) increased by 12% after strong quarterly profit.",
        extractions=[
            lx.data.Extraction(
                extraction_class="organization",
                extraction_text="Tesla"
            ),
            lx.data.Extraction(
                extraction_class="stock_symbol",
                extraction_text="TSLA"
            ),
            lx.data.Extraction(
                extraction_class="percentage",
                extraction_text="12%"
            ),
            lx.data.Extraction(
                extraction_class="profit_loss",
                extraction_text="profit"
            )
        ]
    ),

    lx.data.ExampleData(
        text="The Federal Reserve increased interest rates affecting global markets.",
        extractions=[
            lx.data.Extraction(
                extraction_class="organization",
                extraction_text="Federal Reserve"
            ),
            lx.data.Extraction(
                extraction_class="economic_indicator",
                extraction_text="interest rates"
            ),
            lx.data.Extraction(
                extraction_class="market_event",
                extraction_text="increased"
            )
        ]
    )
]

# -------------------------------
# 5️⃣ Run Extraction
# -------------------------------
result = lx.extract(
    text_or_documents=TEXT,
    prompt_description=PROMPT,
    examples=EXAMPLES,
    api_key=API_KEY
)

# -------------------------------
# 6️⃣ Print Output
# -------------------------------
for extraction in result.extractions:
    print("Class:", extraction.extraction_class)
    print("Text:", extraction.extraction_text)
    print("Attributes:", extraction.attributes)
    print("-" * 40)

# -------------------------------
# 7️⃣ Save Visualization
# -------------------------------
html_output = lx.visualize(result)

with open("finance_visualization.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ Extraction complete!")
print("Visualization saved as finance_visualization.html")
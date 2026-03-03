import os
from dotenv import load_dotenv
import langextract as lx
from langextract.providers.openai import OpenAILanguageModel
import csv

# 1️⃣ Load API Key
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

# 2️⃣ Setup LLM model
groq_model = OpenAILanguageModel(
    model_id="llama-3.3-70b-versatile",
    api_key=GROQ_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# 3️⃣ Load full invoice text
invoice_file = "docling.txt"
if not os.path.exists(invoice_file):
    print("Error: docling.txt not found!")
    exit()

with open(invoice_file, "r", encoding="utf-8") as f:
    text_content = f.read()

# 4️⃣ Prompt and realistic example
PROMPT = """
Extract the following entities from this invoice text:
- company
- invoice_number
- date
- amount
- tax_percentage
- tax_amount
- total_payable
- account_number
- ifsc_code
- payment_terms
- contact_department
- declaration
Return each entity only if it appears in the text.
"""

EXAMPLES = [
    lx.data.ExampleData(
        text="""
Invoice Number: TATA-INV-2026-001
Date: 02 March 2026
Company: Tata Consultancy Services Limited
Account Number: 9876543210
IFSC Code: TATA0001234
Amount: ₹1,20,000
Tax (18% GST): ₹21,600
Total Payable: ₹1,41,600
Payment Terms: Payment is due within 15 days of the invoice date
Contact Department: Finance Department
Declaration: We hereby certify that the particulars stated above are true and correct
""",
        extractions=[
            lx.data.Extraction(extraction_class="company", extraction_text="Tata Consultancy Services Limited"),
            lx.data.Extraction(extraction_class="invoice_number", extraction_text="TATA-INV-2026-001"),
            lx.data.Extraction(extraction_class="date", extraction_text="02 March 2026"),
            lx.data.Extraction(extraction_class="amount", extraction_text="₹1,20,000"),
            lx.data.Extraction(extraction_class="tax_percentage", extraction_text="18%"),
            lx.data.Extraction(extraction_class="tax_amount", extraction_text="₹21,600"),
            lx.data.Extraction(extraction_class="total_payable", extraction_text="₹1,41,600"),
            lx.data.Extraction(extraction_class="account_number", extraction_text="9876543210"),
            lx.data.Extraction(extraction_class="ifsc_code", extraction_text="TATA0001234"),
            lx.data.Extraction(extraction_class="payment_terms", extraction_text="Payment is due within 15 days of the invoice date"),
            lx.data.Extraction(extraction_class="contact_department", extraction_text="Finance Department"),
            lx.data.Extraction(extraction_class="declaration", extraction_text="We hereby certify that the particulars stated above are true and correct")
        ]
    )
]

# 5️⃣ Extract entities
print("Extracting all invoice entities...")
try:
    results = lx.extract(
        text_or_documents=text_content,
        prompt_description=PROMPT,
        examples=EXAMPLES,
        model=groq_model
    )

    # 6️⃣ HTML visualization
    html_content = lx.visualize(results)
    output_html = html_content.data if hasattr(html_content, 'data') else html_content
    with open("finance_visualization.html", "w", encoding="utf-8") as f:
        f.write(output_html)
    print("HTML visualization saved as 'finance_visualization.html'.")

    # 7️⃣ CSV output (Windows-safe & correct)
    csv_file = "entities.csv"
    extractions = []
    if hasattr(results, "documents") and len(results.documents) > 0:
        extractions = results.documents[0].extractions

    if not extractions:
        print("No entities found. Check your prompt/examples.")
    else:
        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Class", "Text"])
            for e in extractions:
                writer.writerow([e.extraction_class.strip(), e.extraction_text.strip()])
        print(f"Entities saved in '{csv_file}'. Total: {len(extractions)}")

    # Optional: print entities to console for verification
    print("\nExtracted entities:")
    for e in extractions:
        print(f"{e.extraction_class}: {e.extraction_text}")

except Exception as e:
    print(f"Error: {e}")
 
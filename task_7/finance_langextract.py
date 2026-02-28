import os
import textwrap
import langextract as lx

# --- CONFIGURATION ---
# 1. PASTE YOUR GOOGLE API KEY HERE (Keep the quotes!)
GOOGLE_API_KEY = "YOUR GOOGLE API KEY"

# LangExtract looks for this specific environment variable
os.environ["LANGEXTRACT_API_KEY"] = GOOGLE_API_KEY

def main():
    # 2. Define File Paths
    input_file = os.path.join("output", "earnings.txt")
    output_html = os.path.join("output", "finance_ner_dashboard.html")

    if not os.path.exists(input_file):
        print(f"❌ Error: Could not find '{input_file}'")
        return

    print(f"📂 Reading document: {input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        # We reduced this to 3,000 characters to prevent the 429 Rate Limit error
        text_content = f.read()[:3000]

    # 3. Define the Extraction Prompt
    prompt = textwrap.dedent("""\
        Extract all finance-related entities from the earnings call transcript.
        Use exact text from the source for extractions. Do not paraphrase.
        Focus on the following entity classes:
        - 'company': Names of companies or stock tickers.
        - 'metric': Financial metrics, revenue numbers, percentages, or monetary values.
        - 'executive': Names of CEOs, CFOs, or other corporate officers.
        - 'sentiment': Expressions of market outlook or risk (e.g., bullish, headwinds).
        Provide meaningful attributes for each entity.
    """)

    # 4. Provide a "Few-Shot" Example
    examples = [
        lx.data.ExampleData(
            text=(
                "AlphaTech's CEO, Jane Doe, announced a quarterly revenue of $2.5 billion, "
                "exceeding expectations and signaling a strongly bullish outlook."
            ),
            extractions=[
                lx.data.Extraction(
                    extraction_class="company",
                    extraction_text="AlphaTech",
                    attributes={"type": "corporation"}
                ),
                lx.data.Extraction(
                    extraction_class="executive",
                    extraction_text="Jane Doe",
                    attributes={"role": "CEO"}
                ),
                lx.data.Extraction(
                    extraction_class="metric",
                    extraction_text="quarterly revenue of $2.5 billion",
                    attributes={"metric_type": "revenue", "value": "$2.5 billion"}
                ),
                lx.data.Extraction(
                    extraction_class="sentiment",
                    extraction_text="strongly bullish outlook",
                    attributes={"sentiment": "bullish"}
                ),
            ]
        )
    ]

    print("   > 🧠 Running LangExtract (this might take 10-20 seconds)...")
    
    # 5. Execute the Extraction
    try:
        result = lx.extract(
            text_or_documents=text_content,
            prompt_description=prompt,
            examples=examples,
            model_id="gemini-2.5-flash" # Using the fast Gemini model
        )
        
        # 6. Print Results to Terminal
        print("\n==================================================")
        print("          FINANCIAL ENTITIES EXTRACTED            ")
        print("==================================================")
        for ext in result.extractions:
            print(f"📌 [{ext.extraction_class.upper()}] {ext.extraction_text}")
            if ext.attributes:
                print(f"   ↳ Attributes: {ext.attributes}")
        
        # 7. Generate Interactive HTML Dashboard
        print("\n   > 📊 Generating visualization dashboard...")
        html_content = lx.visualize(result)
        
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"✅ Success! Interactive dashboard saved to: {output_html}")
        print("   (Open this HTML file in your web browser to see the results)")
        
    except Exception as e:
        print(f"❌ Extraction Error: {e}")

if __name__ == "__main__":
    main()
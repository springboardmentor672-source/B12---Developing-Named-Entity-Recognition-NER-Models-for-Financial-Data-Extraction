import os
import re
import langextract as lx
from langextract.providers.openai import OpenAILanguageModel
from configg import GROQ_API_KEY

if not GROQ_API_KEY:
    raise ValueError(" GROQ_API_KEY missing in configg.py")

#  Initialize Groq Model

model = OpenAILanguageModel(
    model_id="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

#  Read Markdown File

file_path = "files.md"

if not os.path.exists(file_path):
    raise FileNotFoundError("files.md not found")

with open(file_path, "r", encoding="utf-8") as f:
    raw_text = f.read()

def clean_markdown(text):
    text = re.sub(r"#.*", "", text)
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
clean_text = clean_markdown(raw_text)
clean_text = clean_text[:4000]   # safe token limit

# Strict Extraction Instruction
instruction = """
Extract entities using ONLY the following labels:

- company
- money
- percentage
- date
- financial_metric

Definitions:
company → Business or corporate names
money → Dollar or currency amounts
percentage → Values like 10%, 5.5%
date → Any year or full date
financial_metric → Revenue, profit, EBITDA, net income, etc.

Do not create any other labels.
"""

#  Few-shot Examples

examples = [
    lx.data.ExampleData(
        text="Amazon reported $5 billion revenue in 2023 with 15% growth.",
        extractions=[
            lx.data.Extraction("company", "Amazon"),
            lx.data.Extraction("money", "$5 billion"),
            lx.data.Extraction("financial_metric", "revenue"),
            lx.data.Extraction("date", "2023"),
            lx.data.Extraction("percentage", "15%")
        ]
    )
]

print(" Running Financial Entity Extraction...\n")

try:
    result = lx.extract(
        text_or_documents=clean_text,
        prompt_description=instruction,
        examples=examples,
        model=model
    )

    print(f"Total Entities Found: {len(result.extractions)}")

    # Show detected labels
    labels = set([e.extraction_class for e in result.extractions])
    print("Labels detected:", labels)

    #  Generate HTML

    html_content = lx.visualize(result)
    final_html = html_content.data if hasattr(html_content, "data") else html_content

    output_file = "finance_md_visualization.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"\n HTML file created: {output_file}")
    print(" Open it in Chrome / Edge to see colored highlights.")

except Exception as e:
    print(" Error:", e)
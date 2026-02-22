import pdfplumber
from transformers import pipeline
import pandas as pd

# 1. Load PDF file
pdf_path = "finance.pdf"

text_data = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text_data += page.extract_text() + "\n"

# Split text into sentences
sentences = text_data.split(".")

# 2. Load NER Model
ner_model = pipeline(
    "ner",
    model="Sirius35/Fintuned-distilbert-NER-for-FinTech",
    aggregation_strategy="simple"
)

# 3. Store results
all_findings = []

print("Running NER on PDF...")

# 4. Process each sentence
for i, sentence in enumerate(sentences):
    if sentence.strip() == "":
        continue

    results = ner_model(sentence)

    for ent in results:
        all_findings.append({
            "Sentence_ID": i,
            "Word": ent['word'].replace("##", ""),
            "Label": ent['entity_group'],
            "Confidence": ent['score']
        })

# 5. Save output to Markdown (.md)
df = pd.DataFrame(all_findings)
df.to_markdown("ner_results_from_pdf.md", index=False)

print("\n--- DONE ---")
print(f"Total entities found: {len(df)}")
print("Results saved to: ner_results_from_pdf.md")
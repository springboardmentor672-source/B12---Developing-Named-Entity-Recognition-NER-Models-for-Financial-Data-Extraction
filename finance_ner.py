from transformers import pipeline

ner = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)

with open("financial_report.txt", "r", encoding="utf-8") as file:
    text = file.read()

max_chunk = 400
chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]

all_results = []

for chunk in chunks:
    results = ner(chunk)
    all_results.extend(results)
    
for entity in all_results:
    print("Entity:", entity["word"])
    print("Type:", entity["entity_group"])
    print("Confidence:", round(entity["score"], 4))
    print("----------------------")

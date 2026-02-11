from transformers import pipeline
import re


MODEL_NAME = "Jean-Baptiste/roberta-large-ner-english"

ner_pipeline = pipeline(
    "ner",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME,
    aggregation_strategy="simple"
)

def read_markdown_file(file_path: str) -> str:
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_entities(text: str, entity_group: list = None) -> list:
   
    entities = ner_pipeline(text)
    entity_list = []

    for entity in entities:
        word = entity["word"].strip()

        # Remove punctuation-only entities (e.g., ".", ",")
        if re.fullmatch(r"[^\w]+", word):
            continue

        entity_dict = {
            "entity_group": entity["entity_group"],
            "word": word,
            "start": entity["start"],
            "end": entity["end"],
            "score": float(entity["score"])
        }

        if entity_group is None or entity["entity_group"] in entity_group:
            entity_list.append(entity_dict)

    return entity_list


if __name__ == "__main__":
    # Path to Docling-generated Markdown file
    md_file_path = "apple_report.md"  

    # Read text from Markdown
    text = read_markdown_file(md_file_path)

    # Extract entities
    results = extract_entities(text)

    # Print results
    for r in results:
        print(r)

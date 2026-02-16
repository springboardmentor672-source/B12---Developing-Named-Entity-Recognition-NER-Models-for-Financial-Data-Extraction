from transformers import pipeline
import re

# Loading NER pipeline
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

def extract_entities(text: str) -> list:
    entities = ner_pipeline(text)
    entity_list = []

    for entity in entities:
        word = entity["word"].strip()

        # Removing punctuation-only entities
        if re.fullmatch(r"[^\w]+", word):
            continue

        entity_dict = {
            "Entity Type": entity["entity_group"],
            "Text": word,
            "Start": entity["start"],
            "End": entity["end"]
        }

        entity_list.append(entity_dict)

    return entity_list


if __name__ == "__main__":
    md_file_path = "input.md"   # input markdown file

    text = read_markdown_file(md_file_path)

    results = extract_entities(text)

    print("\nExtracted Entities:\n")

    for r in results:
        print(r)

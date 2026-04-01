from transformers import pipeline
import re

# Load model once
ner_pipeline = pipeline(
    "ner",
    model="Jean-Baptiste/roberta-large-ner-english",
    tokenizer="Jean-Baptiste/roberta-large-ner-english",
    aggregation_strategy="simple"
)

def extract_entities(text: str):
    entities = ner_pipeline(text)
    result = []

    for e in entities:
        word = e["word"].strip()

        if re.fullmatch(r"[^\w]+", word):
            continue

        result.append({
            "entity": e["entity_group"],
            "text": word,
            "score": float(e["score"])
        })

    return result
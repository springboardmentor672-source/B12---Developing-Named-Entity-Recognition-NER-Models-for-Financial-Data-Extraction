import spacy
from transformers import pipeline

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Financial-domain NER model (BERT)
finance_ner = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)


def chunk_text(text, max_words=400):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])


def combined_financial_ner(text):
    results = {
        "financial_entities": [],
        "general_entities": []
    }

    # --------------------------
    # 1️⃣ Financial NER (Transformer)
    # --------------------------
    for chunk in chunk_text(text):
        financial_entities = finance_ner(chunk)

        for ent in financial_entities:
            results["financial_entities"].append({
                "text": ent["word"],
                "label": ent["entity_group"],
                "confidence": round(ent["score"], 3)
            })

    # --------------------------
    # 2️⃣ General NER (spaCy)
    # --------------------------
    doc = nlp(text)

    for ent in doc.ents:
        results["general_entities"].append({
            "text": ent.text,
            "label": ent.label_
        })

    return results
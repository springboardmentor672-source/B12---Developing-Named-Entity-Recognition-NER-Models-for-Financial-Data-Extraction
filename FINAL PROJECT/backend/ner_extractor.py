from transformers import pipeline

MODEL_NAME = "dslim/bert-base-NER"
ner_pipeline = pipeline("ner", model=MODEL_NAME, tokenizer=MODEL_NAME, aggregation_strategy="simple")

def extract_entities(text: str, entity_group: list = None) -> list:

    entities = ner_pipeline(text)
    
    entity_list = []
    for entity in entities:
        entity_dict = {
            "entity_group": entity["entity_group"],
            "word": entity["word"],
            "start": entity["start"],
            "end": entity["end"],
            "score": float(entity["score"])
        }
        if entity_group is None or entity["entity_group"] in entity_group:
            entity_list.append(entity_dict)
    
    return entity_list

if __name__ == "__main__":
    sample_text = """Sundar Pichai, CEO, said: “We’re pleased with our strong Q1 results, which reflect healthy growth and momentum
across the business. Underpinning this growth is our unique full stack approach to AI. This quarter was super exciting
as we rolled out Gemini 2.5, our most intelligent AI model, which is achieving breakthroughs in performance and is
an extraordinary foundation for our future innovation. Search saw continued strong growth, boosted by the
engagement we’re seeing with features like AI Overviews, which now has 1.5 billion users per month. Driven by
YouTube and Google One, we surpassed 270 million paid subscriptions. And Cloud grew rapidly with significant
demand for our solutions.”"""
    # entities = extract_entities(sample_text)
    entities = extract_entities(sample_text,entity_group=["ORG","PER", "LOC"])
    print(entities)
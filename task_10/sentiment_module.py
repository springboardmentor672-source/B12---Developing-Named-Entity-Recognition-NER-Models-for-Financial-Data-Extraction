from transformers import pipeline
import re

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert"
)

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)

def analyze_sentiment(text):
    sentences = split_sentences(text)
    results = []

    for s in sentences:
        if len(s.strip()) < 10:
            continue

        output = sentiment_pipeline(s[:512])[0]

        results.append({
            "sentence": s,
            "sentiment": output["label"],
            "confidence": float(output["score"])
        })

    return results
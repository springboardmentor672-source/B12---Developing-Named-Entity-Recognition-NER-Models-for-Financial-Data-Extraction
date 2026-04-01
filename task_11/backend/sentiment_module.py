from transformers import pipeline
import re
from collections import Counter

# Load model once
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

    # ---------------- AGGREGATION ----------------
    sentiment_labels = [r["sentiment"] for r in results]
    counts = Counter(sentiment_labels)

    total = len(results)

    if total > 0:
        avg_score = sum(r["confidence"] for r in results) / total
        dominant = max(counts, key=counts.get)
    else:
        avg_score = 0.0
        dominant = "neutral"

    summary = {
        "total_sentences": total,
        "counts": dict(counts),  # convert Counter → JSON-friendly
        "dominant_sentiment": dominant,
        "average_confidence": round(avg_score, 4)
    }

    return {
        "sentence_results": results,
        "summary": summary
    }
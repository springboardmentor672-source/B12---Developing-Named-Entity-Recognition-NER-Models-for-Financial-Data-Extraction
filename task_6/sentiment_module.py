import re
from transformers import pipeline
from collections import Counter

# Load FinBERT model
finbert = pipeline(
    "text-classification",
    model="ProsusAI/finbert"
)


def clean_text(text):
    """
    Light cleaning of extracted PDF text
    """
    text = re.sub(r"\s+", " ", text)  # normalize whitespace
    return text.strip()


def split_into_segments(text):
    """
    Robust segmentation for financial reports
    Splits using line breaks and punctuation.
    """
    segments = []

    # Split by line breaks first
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if len(line) < 25:
            continue

        # Split by punctuation if exists
        parts = re.split(r"[.!?]", line)

        for part in parts:
            part = part.strip()
            if len(part) > 25:
                segments.append(part)

    return segments


def analyze_sentiment(text):
    """
    Runs FinBERT sentiment classification.
    """
    cleaned = clean_text(text)
    segments = split_into_segments(cleaned)

    print("Total extracted segments:", len(segments))

    results = []

    for segment in segments:
        prediction = finbert(segment)[0]

        results.append({
            "sentence": segment,
            "sentiment": prediction["label"],
            "confidence": round(prediction["score"], 3)
        })

    return results


def generate_structured_report(results):
    """
    Generates structured financial sentiment report.
    """

    total = len(results)

    if total == 0:
        return {
            "summary": "No meaningful sentences detected.",
            "high_risk_statements": [],
            "positive_indicators": []
        }

    labels = [r["sentiment"] for r in results]
    count = Counter(labels)

    report = {
        "summary": {
            "total_sentences": total,
            "positive": {
                "count": count["positive"],
                "percentage": round((count["positive"] / total) * 100, 2)
            },
            "negative": {
                "count": count["negative"],
                "percentage": round((count["negative"] / total) * 100, 2)
            },
            "neutral": {
                "count": count["neutral"],
                "percentage": round((count["neutral"] / total) * 100, 2)
            }
        },
        "high_risk_statements": [
            r for r in results
            if r["sentiment"] == "negative" and r["confidence"] > 0.8
        ],
        "positive_indicators": [
            r for r in results
            if r["sentiment"] == "positive" and r["confidence"] > 0.7
        ]
    }

    return report
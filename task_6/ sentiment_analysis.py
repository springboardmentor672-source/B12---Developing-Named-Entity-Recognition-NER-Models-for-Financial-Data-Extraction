import warnings
import re
from transformers import pipeline

# Ignore warnings
warnings.filterwarnings("ignore")

# Load FinBERT
MODEL_NAME = "ProsusAI/finbert"

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME,
    truncation=True,
    max_length=512
)


# -------------------------
# Read File
# -------------------------
def read_document(path):

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def split_sentences(text):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    clean = []

    for s in sentences:
        if len(s.strip()) > 5:
            clean.append(s.strip())

    return clean


# -------------------------
# Analyze Sentiment
# -------------------------
def analyze_sentiment(text):

    sentences = split_sentences(text)

    results = []

    for sentence in sentences:

        try:
            output = sentiment_pipeline(sentence)[0]

            results.append({
                "sentence": sentence,
                "label": output["label"].lower(),
                "score": round(float(output["score"]), 4)
            })

        except:
            continue

    return results


# -------------------------
# Report
# -------------------------
def generate_report(results):

    positive = []
    negative = []
    neutral = []

    for r in results:

        if r["label"] == "positive":
            positive.append(r)

        elif r["label"] == "negative":
            negative.append(r)

        else:
            neutral.append(r)

    total = len(results)

    print("\n📊 Financial Sentiment Analysis Report\n")

    print(f"Total Sentences : {total}")
    print(f"Positive        : {len(positive)}")
    print(f"Negative        : {len(negative)}")
    print(f"Neutral         : {len(neutral)}")

    print("\n" + "-" * 60)

    # Positive
    print("\n🟢 Positive Examples:")
    for i, r in enumerate(positive[:2], 1):
        print(f"{i}. Sentence  : {r['sentence']}")
        print(f"   Confidence: {r['score']}\n")

    # Negative
    print("\n🔴 Negative Examples:")
    for i, r in enumerate(negative[:2], 1):
        print(f"{i}. Sentence  : {r['sentence']}")
        print(f"   Confidence: {r['score']}\n")

    # Neutral
    print("\n⚪ Neutral Examples:")
    for i, r in enumerate(neutral[:2], 1):
        print(f"{i}. Sentence  : {r['sentence']}")
        print(f"   Confidence: {r['score']}\n")

    print("-" * 60)


# -------------------------
# Main
# -------------------------
def main():

    print("\nRunning sentiment analysis...\n")

    file_path = "docling.txt"

    text = read_document(file_path)

    results = analyze_sentiment(text)

    generate_report(results)


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    main()

import os
import re
import nltk
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from collections import Counter

nltk.download('punkt')

print("Loading FinBERT model...")

financial_sentiment = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

file_path = r"C:\Users\pc\OneDrive\Desktop\new\Finance_NER_Project\FinanceInsight\output.md"

if not os.path.exists(file_path):
    print("File not found.")
    exit()

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()


text = re.sub(r'[#*_>`\-]', '', text)
text = re.sub(r'\n+', ' ', text)

sentences = sent_tokenize(text)

valid_sentences = [
    s.strip() for s in sentences
    if len(s.strip()) > 60
]

print("\nSENTENCE LEVEL SENTIMENT ANALYSIS\n")

sentiment_counts = Counter()
confidence_scores = []

for i in range(0, len(valid_sentences), 32):

    batch = valid_sentences[i:i+32]

    batch_results = financial_sentiment(
        batch,
        truncation=True,
        max_length=128
    )

    for sentence, result in zip(batch, batch_results):
        label = result["label"].lower()
        score = result["score"]

        sentiment_counts[label] += 1
        confidence_scores.append(score)

        clean_sentence = sentence.replace(",", " ")

        print("Sentence:", clean_sentence)
        print("Label:", label)
        print("Score:", f"{score:.4f}")
        print("-" * 80)

    print(f"Processed {min(i+32, len(valid_sentences))}/{len(valid_sentences)}\n")


total = sum(sentiment_counts.values())

positive = sentiment_counts["positive"]
negative = sentiment_counts["negative"]
neutral = sentiment_counts["neutral"]

positive_pct = (positive / total) * 100 if total > 0 else 0
negative_pct = (negative / total) * 100 if total > 0 else 0
neutral_pct = (neutral / total) * 100 if total > 0 else 0

if positive_pct > negative_pct:
    overall = "POSITIVE"
elif negative_pct > positive_pct:
    overall = "NEGATIVE"
else:
    overall = "NEUTRAL"

avg_conf = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0

print("\nEXECUTIVE SUMMARY")
print("--------------------------------")
print(f"Total Sentences   : {total}")
print(f"Positive Sentiment: {positive} ({positive_pct:.2f}%)")
print(f"Negative Sentiment: {negative} ({negative_pct:.2f}%)")
print(f"Neutral Sentiment : {neutral} ({neutral_pct:.2f}%)")
print("--------------------------------")
print(f"Overall Sentiment : {overall}")
print(f"Average Confidence: {avg_conf:.4f}")

print("\nAnalysis Completed Successfully.")

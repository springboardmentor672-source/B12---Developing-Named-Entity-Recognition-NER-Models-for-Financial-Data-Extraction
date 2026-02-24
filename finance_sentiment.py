import nltk
from transformers import pipeline
import fitz
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

nltk.download("punkt", quiet=True)

MODEL_NAME = "ProsusAI/finbert"
sentiment_pipeline = pipeline("sentiment-analysis", model=MODEL_NAME, tokenizer=MODEL_NAME)

# -------- PDF TEXT EXTRACTION --------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# -------- SENTENCE SPLITTING --------
def split_sentences(text):
    return nltk.sent_tokenize(text)

# -------- SENTIMENT ANALYSIS --------
def analyze_sentiment(sentences, max_length=400):
    results = []

    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 10:
            continue

        for i in range(0, len(sent), max_length):
            chunk = sent[i:i + max_length]

            try:
                res = sentiment_pipeline(chunk)[0]
                results.append({
                    "sentence": chunk,
                    "label": res["label"],
                    "score": round(res["score"] * 100, 2)
                })
            except Exception as e:
                print("Skipping chunk due to error:", e)

    return results

# -------- TERMINAL REPORT --------

def print_report(results):

    total = len(results)
    pos = sum(1 for r in results if r["label"] == "positive")
    neg = sum(1 for r in results if r["label"] == "negative")
    neu = sum(1 for r in results if r["label"] == "neutral")

    # ---- Calculate Overall Sentiment ----
    sentiment_counts = {
        "positive": pos,
        "negative": neg,
        "neutral": neu
    }

    overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)

    # Average confidence of dominant class
    dominant_scores = [r["score"] for r in results if r["label"] == overall_sentiment]
    overall_confidence = round(sum(dominant_scores) / len(dominant_scores), 2) if dominant_scores else 0

    print("\n" + "="*60)
    print("📊 FINANCIAL SENTIMENT ANALYSIS REPORT")
    print("="*60)

    print("\n🧾 Executive Summary")
    print(f"Total Sentences : {total}")
    print(f"🟢 Positive      : {pos}")
    print(f"🔴 Negative      : {neg}")
    print(f"⚪ Neutral       : {neu}")

    print("\n📌 Overall Document Sentiment")
    print(f"Positive % : {round((pos/total)*100,2)}%")
    print(f"Negative % : {round((neg/total)*100,2)}%")
    print(f"Neutral  % : {round((neu/total)*100,2)}%")
    print(f"\n🏆 Final Overall Sentiment : {overall_sentiment.upper()}")
    print(f"🔥 Overall Confidence      : {overall_confidence}%")

    print("\n🟢 Positive Highlights")
    for r in results:
        if r["label"] == "positive":
            print(f"- {r['score']}% Confidence : {r['sentence']}")

    print("\n🔴 Negative Risks")
    for r in results:
        if r["label"] == "negative":
            print(f"- {r['score']}% Confidence : {r['sentence']}")

    print("\n⚪ Neutral Statements")
    for r in results:
        if r["label"] == "neutral":
            print(f"- {r['score']}% Confidence : {r['sentence']}")

# -------- MAIN --------
if __name__ == "__main__":

    pdf_path = "finance.pdf"   # change name if needed

    print("\n📄 Reading PDF...")
    text = extract_text_from_pdf(pdf_path)

    print("✂ Splitting into sentences...")
    sentences = split_sentences(text)

    print("🤖 Performing sentiment analysis...")
    results = analyze_sentiment(sentences)

    print_report(results)
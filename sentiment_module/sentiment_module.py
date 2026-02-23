import re
from transformers import pipeline

# Loading Finbert Model
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert",
    truncation=True,
    max_length=512
)

# Reading Markdown File
def read_md(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Cleaning Text
def clean_text(text):

    text = re.sub(r'\|.*?\|', ' ', text)
    text = re.sub(r'GLYPH.*', ' ', text)
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\b[\d,()\- ]{5,}\b', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# Valid Sentence Checking
def is_valid_sentence(sentence):

    sentence = sentence.strip()

    if len(sentence) < 10:
        return False

    if re.fullmatch(r'[\d\W_ ]+', sentence):
        return False

    if sentence.count('|') > 3:
        return False

    return True

# Splitting into sentences
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s for s in sentences if is_valid_sentence(s)]

# Sentiment Analysis
def analyze_sentiment(sentences):

    results = []

    pos_count = 0
    neg_count = 0
    neu_count = 0

    total_confidence = 0

    for sentence in sentences:
        try:
            output = sentiment_pipeline(sentence[:512])[0]

            sentiment = output["label"].lower()
            confidence = round(output["score"], 4)

            total_confidence += confidence

            if sentiment == "positive":
                pos_count += 1
            elif sentiment == "negative":
                neg_count += 1
            else:
                neu_count += 1

            results.append((sentence, sentiment, confidence))

        except Exception as e:
            print("Error:", e)

    overall_confidence = round(total_confidence / len(results), 4) if results else 0

    return results, pos_count, neg_count, neu_count, overall_confidence


# Main
if __name__ == "__main__":

    file_path = "input.md"

    raw_text = read_md(file_path)
    cleaned_text = clean_text(raw_text)
    sentences = split_sentences(cleaned_text)

    results, pos, neg, neu, overall_conf = analyze_sentiment(sentences)

    # Printing Summary
    print("\n========== DOCUMENT SUMMARY ==========\n")

    print("Total Positive Sentences:", pos)
    print("Total Neutral Sentences:", neu)
    print("Total Negative Sentences:", neg)
    print("\nOverall Document Confidence Score:", overall_conf)

    print("\n======================================\n")

    # Printing Sentence Results
    for sentence, sentiment, confidence in results:
        print("Sentence:", sentence)
        print("Sentiment:", sentiment)
        print("Confidence:", confidence)
        print("-" * 80)
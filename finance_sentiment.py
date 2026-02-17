import os
import torch
import nltk
import pandas as pd
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Download tokenizer (only first time)
nltk.download('punkt')

# =====================================
# 1️⃣ Load FinBERT Model
# =====================================
model_name = "ProsusAI/finbert"

print("Loading FinBERT model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

labels = ["negative", "neutral", "positive"]

# =====================================
# 2️⃣ Read Finance Document
# =====================================
def load_document(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

# =====================================
# 3️⃣ Analyze Sentiment
# =====================================
def analyze_document(text):

    sentences = nltk.sent_tokenize(text)

    results = []

    for sentence in sentences:

        inputs = tokenizer(sentence, return_tensors="pt", truncation=True)
        outputs = model(**inputs)

        probs = F.softmax(outputs.logits, dim=1)
        confidence, predicted_class = torch.max(probs, dim=1)

        label = labels[predicted_class.item()]
        score = confidence.item()

        results.append({
            "Sentence": sentence,
            "Sentiment": label,
            "Confidence": round(score, 4)
        })

    return results

# =====================================
# 4️⃣ Save Results
# =====================================
def save_results(results, output_path):
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)
    print(f"\nResults saved to {output_path}")

# =====================================
# 5️⃣ Main Execution
# =====================================
if __name__ == "__main__":

    input_path = "data/samples.txt"
    output_path = "outputs/results.csv"

    text = load_document(input_path)

    print("\nAnalyzing document...\n")

    results = analyze_document(text)

    for r in results:
        print(f"Sentence: {r['Sentence']}")
        print(f"Sentiment: {r['Sentiment']}")
        print(f"Confidence: {r['Confidence']}")
        print("-" * 50)

    save_results(results, output_path)

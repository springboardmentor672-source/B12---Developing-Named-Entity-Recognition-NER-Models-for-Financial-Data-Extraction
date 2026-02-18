import re
import nltk
from transformers import pipeline


nltk.download("punkt", quiet=True)

MODEL_NAME = "ProsusAI/finbert"
sentiment_model = pipeline("sentiment-analysis", model=MODEL_NAME)

def clean_text(text: str) -> str:
    text = re.sub(r'\|', ' ', text)       
    text = re.sub(r'-{2,}', ' ', text)    
    text = re.sub(r'\s+', ' ', text)       
    return text.strip()

def analyze_file(file_path: str):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    text = clean_text(text)
    sentences = nltk.sent_tokenize(text)

    for sentence in sentences:

        sentence = sentence.strip()
    
        if len(sentence) < 15:
            continue
        if not any(c.isalpha() for c in sentence):
            continue

        result = sentiment_model(sentence[:512])[0]

        print(f"Sentence: {sentence}")
        print(f"Label: {result['label']}")
        print(f"Score: {round(result['score'],4)}")
        print()

if __name__ == "__main__":
    analyze_file("output.md")

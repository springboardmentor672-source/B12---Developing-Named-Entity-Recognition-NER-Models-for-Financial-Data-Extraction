from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil, os
from textblob import TextBlob
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads folder
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ✅ LOAD MODEL (YOU MISSED THIS)
ner_model = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)

# ✅ FIXED NER FUNCTION
def ner_analysis(text):
    results = ner_model(text)   # ✅ correct

    cleaned = []

    for ent in results:
        cleaned.append({
            "text": ent["word"],
            "label": ent["entity_group"],
            "confidence": float(ent["score"])  # convert to float
        })

    return cleaned

# Read file
def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Sentiment
def sentiment_analysis(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    return {
        "sentiment": "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral",
        "polarity": polarity
    }

# Finance
def finance_extractor(text):
    keywords = {
         "Invoice": ["invoice", "invoice number"],
    "Payment": ["payment", "due", "transfer"],
    "Amount": ["amount", "total", "payable"],
    "Tax": ["tax", "gst"],
    "Banking": ["account", "ifsc", "bank"],
    "Company": ["company", "services"],
    "Finance Terms": ["interest", "charges", "billing"]
    }

    result = {}
    text = text.lower()

    for k, words in keywords.items():
        found = [w for w in words if w in text]
        if found:
            result[k] = found

    return result

# API
@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = read_txt(path)

    return {
        "sentiment": sentiment_analysis(text),
        "ner": ner_analysis(text),
        "finance": finance_extractor(text)
    }
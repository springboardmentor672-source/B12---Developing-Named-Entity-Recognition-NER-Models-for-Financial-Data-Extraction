from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz
from markdownify import markdownify as md
import warnings
import logging
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from groq import Groq
import json
import re
import nltk

# ---------------- BASIC SETUP ----------------
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
nltk.download("punkt", quiet=True)

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "Final Unified API Running"}

# ---------------- ENV ----------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

# ---------------- MODELS ----------------
print("Loading models...")

ner_model = pipeline(
    "ner",
    model="./bert-base-NER",
    aggregation_strategy="simple"
)

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="./finbert"
)

print("Models loaded successfully")

# ---------------- UTILS ----------------
def safe_text(text, limit=10000):   # 🔥 increased limit
    return text[:limit]

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ---------------- NER ----------------
def ner_function(text):
    text = clean_text(safe_text(text))

    try:
        return [
            {
                "word": ent['word'],
                "label": ent['entity_group']
            }
            for ent in ner_model(text)
        ]
    except Exception as e:
        print("NER ERROR:", e)
        return []

# ---------------- SENTIMENT ----------------
def sentiment_function(text):
    text = clean_text(safe_text(text))
    sentences = nltk.sent_tokenize(text)

    results = []
    pos, neg, neu = 0, 0, 0

    for sent in sentences:
        if len(sent.strip()) < 5:
            continue

        try:
            res = sentiment_pipeline(sent)[0]
        except Exception as e:
            print("SENTIMENT ERROR:", e)
            continue

        label = res["label"].upper()
        score = float(res["score"])

        results.append({
            "sentence": sent,
            "label": label,
            "score": score
        })

        if label == "POSITIVE":
            pos += 1
        elif label == "NEGATIVE":
            neg += 1
        else:
            neu += 1

    total = pos + neg + neu

    return {
        "sentence_wise": results,
        "overall": {
            "positive": round((pos/total)*100, 2) if total else 0,
            "negative": round((neg/total)*100, 2) if total else 0,
            "neutral": round((neu/total)*100, 2) if total else 0
        }
    }

# ---------------- GROQ ----------------
def langextract_function(text):
    text = clean_text(safe_text(text, 5000))   # 🔥 increased

    prompt = f"""
Extract ALL possible entities from the text.

Rules:
- Include organization, person, location, currency, date
- Extract as many as possible
- Do NOT miss repeated entities

Return ONLY JSON:

[
  {{"class": "organization", "text": "Infosys"}},
  {{"class": "location", "text": "India"}}
]

Text:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        output = response.choices[0].message.content.strip()

        match = re.search(r"\[.*\]", output, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            return []

    except Exception as e:
        print("GROQ ERROR:", e)
        return []

# ---------------- MAIN API ----------------
@app.post("/full-analysis/")
async def full_analysis(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    try:
        contents = await file.read()
        pdf = fitz.open(stream=contents, filetype="pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF read error: {str(e)}")

    text = ""
    for page in pdf:
        text += page.get_text()

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF")

    return {
        "filename": file.filename,
        "pdf_to_markdown": md(text[:10000]),  # only display limit
        "ner": ner_function(text),
        "sentiment_raw": sentiment_function(text),
        "language_extraction": langextract_function(text)
    }
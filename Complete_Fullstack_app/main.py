from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz
from markdownify import markdownify as md
from transformers import pipeline
import nltk
import warnings
import logging
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import json

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
    return {"message": "Final Unified API Running with Groq"}

# ---------------- LOAD ENV ----------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ---------------- NER ----------------
ner_model = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)

def ner_function(text):
    return [
        {
            "word": ent['word'],
            "label": ent['entity_group'],
            "confidence": float(ent['score'])
        }
        for ent in ner_model(text)
    ]

# ---------------- SENTIMENT ----------------
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

def sentiment_function(text):
    sentences = nltk.sent_tokenize(text)

    results = []
    pos, neg, neu = 0, 0, 0

    for sent in sentences:
        if len(sent.strip()) < 5:
            continue

        res = sentiment_pipeline(sent)[0]
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

    overall = {
        "positive": round((pos/total)*100, 2) if total else 0,
        "negative": round((neg/total)*100, 2) if total else 0,
        "neutral": round((neu/total)*100, 2) if total else 0
    }

    return {
        "sentence_wise": results,
        "overall": overall
    }

# ---------------- GROQ LANGEXTRACT ----------------
def langextract_function(text):
    try:
        prompt = f"""
        Extract entities from the text below.

        STRICT RULES:
        - Return ONLY valid JSON
        - No explanation
        - Format:
        [
          {{"class": "person", "text": "John"}},
          {{"class": "organization", "text": "Infosys"}}
        ]

        TEXT:
        {text[:1000]}
        """

        response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
)

        output = response.choices[0].message.content.strip()

        try:
            return json.loads(output)
        except:
            return output  # fallback if not valid JSON

    except Exception as e:
        return str(e)

# ---------------- FINAL API ----------------
@app.post("/full-analysis/")
async def full_analysis(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    contents = await file.read()
    pdf = fitz.open(stream=contents, filetype="pdf")

    text = ""
    for page in pdf:
        text += page.get_text()

    return {
        "filename": file.filename,
        "pdf_to_markdown": md(text),
        "ner": ner_function(text),
        "sentiment_raw": sentiment_function(text),
        "language_extraction": langextract_function(text)
    }
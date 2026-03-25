from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz
from markdownify import markdownify as md
from transformers import pipeline
import nltk
import warnings
import logging
import os
from dotenv import load_dotenv
import langextract as lx
from huggingface_hub import snapshot_download

warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
nltk.download("punkt", quiet=True)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Final Unified API Running"}

# =========================
# ✅ LOCAL MODEL PATHS
# =========================
NER_MODEL_PATH = "./models/ner"
SENTIMENT_MODEL_PATH = "./models/sentiment"

# =========================
# ✅ DOWNLOAD MODELS LOCALLY (RUNS ONCE)
# =========================
if not os.path.exists(NER_MODEL_PATH):
    snapshot_download(
        repo_id="dslim/bert-base-NER",
        local_dir=NER_MODEL_PATH
    )

if not os.path.exists(SENTIMENT_MODEL_PATH):
    snapshot_download(
        repo_id="distilbert-base-uncased-finetuned-sst-2-english",
        local_dir=SENTIMENT_MODEL_PATH
    )

# =========================
# ✅ NER (LAZY LOAD)
# =========================
ner_model = None

def get_ner_model():
    global ner_model
    if ner_model is None:
        ner_model = pipeline(
            "ner",
            model=NER_MODEL_PATH,
            tokenizer=NER_MODEL_PATH,
            aggregation_strategy="simple"
        )
    return ner_model

def ner_function(text):
    model = get_ner_model()
    return [
        {
            "word": ent['word'],
            "label": ent['entity_group'],
            "confidence": float(ent['score'])
        }
        for ent in model(text[:1000])
    ]

# =========================
# ✅ SENTIMENT (LAZY LOAD)
# =========================
sentiment_model = None

def get_sentiment_model():
    global sentiment_model
    if sentiment_model is None:
        sentiment_model = pipeline(
            "sentiment-analysis",
            model=SENTIMENT_MODEL_PATH,
            tokenizer=SENTIMENT_MODEL_PATH
        )
    return sentiment_model

def sentiment_function(text):
    model = get_sentiment_model()
    sentences = nltk.sent_tokenize(text)
    results = []

    for sent in sentences[:10]:
        if len(sent.strip()) < 5:
            continue
        res = model(sent)[0]
        results.append({
            "sentence": sent,
            "label": res["label"],
            "score": float(res["score"])
        })

    return results

# =========================
# ✅ LANGEXTRACT
# =========================
load_dotenv()
API_KEY = os.getenv("LANGEXTRACT_API_KEY")

PROMPT = """
Extract ANY meaningful entities from the text.

Entity classes:
- person
- organization
- place
- date
- number
- concept
"""

EXAMPLES = [
    lx.data.ExampleData(
        text="John visited Paris in 2022.",
        extractions=[
            lx.data.Extraction(
                extraction_class="person",
                extraction_text="John"
            ),
            lx.data.Extraction(
                extraction_class="place",
                extraction_text="Paris"
            ),
            lx.data.Extraction(
                extraction_class="date",
                extraction_text="2022"
            )
        ]
    )
]

def langextract_function(text):
    try:
        if not API_KEY:
            return {"error": "LANGEXTRACT_API_KEY missing"}

        result = lx.extract(
            text_or_documents=text[:3000],
            prompt_description=PROMPT,
            examples=EXAMPLES,
            api_key=API_KEY
        )

        if hasattr(result, "extractions") and result.extractions:
            return [
                {
                    "class": ext.extraction_class,
                    "text": ext.extraction_text,
                    "attributes": ext.attributes
                }
                for ext in result.extractions
            ]
        else:
            return [{
                "class": "info",
                "text": text[:100],
                "attributes": {}
            }]

    except Exception as e:
        return {"error": str(e)}

# =========================
# ✅ FINAL API
# =========================
@app.post("/full-analysis/")
async def full_analysis(file: UploadFile = File(...)):

    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF allowed")

        contents = await file.read()
        pdf = fitz.open(stream=contents, filetype="pdf")

        text = ""
        for page in pdf:
            text += page.get_text()

        if not text.strip():
            raise HTTPException(status_code=400, detail="No readable text")

        markdown_text = md(text)

        return {
            "filename": file.filename,
            "pdf_to_markdown": markdown_text[:2000],
            "ner": ner_function(text),
            "sentiment": sentiment_function(text),
            "language_extraction": langextract_function(text)
        }

    except Exception as e:
        return {"error": str(e)}
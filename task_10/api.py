import os
import fitz
import langextract as lx

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from langextract.providers.openai import OpenAILanguageModel
from transformers import pipeline

# =====================================
# INIT
# =====================================
app = FastAPI(title="Finance AI API")

print("🔹 Loading environment...")
load_dotenv()

GROQ_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")

if not GROQ_KEY:
    raise ValueError("❌ OPENAI_API_KEY missing in .env")

print("✅ Environment loaded")


# =====================================
# MODEL SETUP (NER)
# =====================================
print("🔹 Connecting to Groq model...")

model = OpenAILanguageModel(
    model_id="llama-3.3-70b-versatile",
    api_key=GROQ_KEY,
    base_url=BASE_URL,
    temperature=0.1
)

print("✅ Model ready")


# =====================================
# SENTIMENT MODEL
# =====================================
print("🔹 Loading sentiment model...")
sentiment_pipeline = pipeline("sentiment-analysis")
print("✅ Sentiment model ready")


# =====================================
# PDF → MARKDOWN
# =====================================
def convert_pdf_to_md(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    md_text = ""

    for i, page in enumerate(doc):
        md_text += f"\n\n# Page {i+1}\n\n"
        md_text += page.get_text()

    doc.close()
    return md_text


# =====================================
# NER FUNCTION
# =====================================
def extract_entities(text):

    examples = [
        lx.data.ExampleData(
            text="Tesla reported revenue growth of 25%.",
            extractions=[
                lx.data.Extraction("organization", "Tesla"),
                lx.data.Extraction("financial_metric", "revenue"),
                lx.data.Extraction("growth_rate", "25%")
            ]
        )
    ]

    PROMPT = """
    Extract:
    - organization (company names)
    - financial_metric (revenue, profit, net income)
    - growth_rate (percentages like 10%, 25%)

    Return only entities found.
    """

    results = lx.extract(
        text[:3000],
        PROMPT,
        examples,
        model=model
    )

    return [
        {
            "entity": e.extraction_class,
            "value": e.extraction_text
        }
        for e in results.extractions
    ]


# =====================================
# SENTIMENT FUNCTION
# =====================================
def analyze_sentiment(text):

    sentences = text.split(".")[:10]

    results = []
    for sentence in sentences:
        if sentence.strip():
            res = sentiment_pipeline(sentence)[0]
            results.append({
                "text": sentence.strip(),
                "sentiment": res["label"],
                "score": float(res["score"])
            })

    return results


# =====================================
# API 1 — PDF → MD
# =====================================
@app.post("/convert-pdf-to-md/")
async def convert_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF allowed"})

    pdf_bytes = await file.read()
    md_text = convert_pdf_to_md(pdf_bytes)

    return {
        "filename": file.filename,
        "markdown": md_text[:2000]
    }


# =====================================
# API 2 — FULL ANALYSIS
# =====================================
@app.post("/analyze-document/")
async def analyze_document(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF allowed"})

    try:
        pdf_bytes = await file.read()

        # Step 1: Convert
        md_text = convert_pdf_to_md(pdf_bytes)

        # Step 2: NER
        entities = extract_entities(md_text)

        # Step 3: Sentiment
        sentiment = analyze_sentiment(md_text)

        return {
            "filename": file.filename,
            "entities": entities,
            "sentiment": sentiment
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
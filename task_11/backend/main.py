from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import tempfile
import os
from pathlib import Path

# Import your modules
from ner_module import extract_entities
from sentiment_module import analyze_sentiment
from langextract_module import extract_finance_entities
from document_converter import convert_document

app = FastAPI(title="Finance AI API 🚀")

# ---------------- CORS (for frontend) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PATH SETUP ----------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
CONVERTED_DOCS_DIR = PROJECT_ROOT / "data" / "processed"

# ---------------- PDF PROCESSING ----------------
async def process_pdf(file: UploadFile):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    tmp_path = None

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Convert PDF → Markdown
        markdown_text = convert_document(
            tmp_path,
            output_dir=str(CONVERTED_DOCS_DIR)
        )

        return file.filename, markdown_text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ---------------- CONVERT ONLY ----------------
@app.post("/convert-pdf")
async def convert_pdf(file: UploadFile = File(...)):
    filename, markdown_text = await process_pdf(file)

    return JSONResponse(content={
        "status": "success",
        "filename": filename,
        "markdown_text": markdown_text
    })


# ---------------- NER ----------------
@app.post("/ner")
async def ner_api(file: UploadFile = File(...)):
    filename, text = await process_pdf(file)

    entities = extract_entities(text)

    return JSONResponse(content={
        "status": "success",
        "filename": filename,
        "total_entities": len(entities),
        "entities": entities
    })


# ---------------- SENTIMENT ----------------
@app.post("/sentiment")
async def sentiment_api(file: UploadFile = File(...)):
    filename, text = await process_pdf(file)

    sentiment_data = analyze_sentiment(text)

    return JSONResponse(content={
        "status": "success",
        "filename": filename,
        "sentiment": sentiment_data
    })


# ---------------- LANGEXTRACT ----------------
@app.post("/langextract")
async def langextract_api(file: UploadFile = File(...)):
    filename, text = await process_pdf(file)

    try:
        result = extract_finance_entities(text)

        return JSONResponse(content={
            "status": "success",
            "filename": filename,
            "total_entities": len(result),
            "entities": result
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- ANALYZE ALL ----------------
@app.post("/analyze-all")
async def analyze_all(file: UploadFile = File(...)):
    filename, text = await process_pdf(file)

    # NER
    ner_entities = extract_entities(text)

    # Sentiment (UPDATED ✅)
    sentiment_data = analyze_sentiment(text)

    # LangExtract
    try:
        lang_entities = extract_finance_entities(text)
    except:
        lang_entities = []

    return JSONResponse(content={
        "status": "success",
        "filename": filename,
        "ner": {
            "total": len(ner_entities),
            "entities": ner_entities
        },
        "sentiment": sentiment_data,
        "langextract": {
            "total": len(lang_entities),
            "entities": lang_entities
        }
    })


# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {
        "message": "Finance AI API Running ✅",
        "endpoints": [
            "/convert-pdf",
            "/ner",
            "/sentiment",
            "/langextract",
            "/analyze-all"
        ]
    }
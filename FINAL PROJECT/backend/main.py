from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import tempfile
import os
from pathlib import Path
from document_converter import convert_document
from ner_extractor import extract_entities
from langextract_service import extract_financial_info
from sentiment_analysis import analyze_sentiment

app = FastAPI(title="NER Project API")

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
CONVERTED_DOCS_DIR = PROJECT_ROOT / "data" / "converted_docs"


async def process_pdf(file: UploadFile) -> tuple[str, str]:
    """Validate PDF, convert to markdown, return (filename, markdown_text)."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    tmp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        markdown_text = convert_document(tmp_file_path, output_dir=str(CONVERTED_DOCS_DIR))
        return file.filename, markdown_text

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    finally:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)


@app.post("/convert-pdf")
async def convert_pdf_to_markdown(file: UploadFile = File(...)):
    """Convert PDF to Markdown - utility endpoint."""
    filename, markdown_text = await process_pdf(file)
    return JSONResponse(content={
        "filename": filename,
        "status": "success",
        "markdown_text": markdown_text
    })


@app.post("/ner")
async def ner_endpoint(
    file: UploadFile = File(...),
    entity_groups: str = Query(default=None, description="Comma-separated entity types: ORG,PER,LOC,MISC")
):
    """Extract named entities from PDF using BERT NER."""
    filename, markdown_text = await process_pdf(file)

    entity_filter = None
    if entity_groups:
        entity_filter = [g.strip().upper() for g in entity_groups.split(",")]

    entities = extract_entities(markdown_text, entity_group=entity_filter)

    return JSONResponse(content={
        "status": "success",
        "filename": filename,
        "markdown_text": markdown_text,
        "total_entities": len(entities),
        "entities": entities
    })


@app.post("/langextract")
async def langextract_endpoint(
    file: UploadFile = File(...),
    model_id: str = Query(default="gemini-3-flash-preview", description="Gemini model ID"),
    extraction_passes: int = Query(default=1, ge=1, le=3, description="Number of extraction passes"),
    save_results: bool = Query(default=False, description="Save results to JSONL")
):
    """Extract financial entities from PDF using LangExtract + Gemini AI."""
    filename, markdown_text = await process_pdf(file)

    try:
        result = extract_financial_info(
            text=markdown_text,
            model_id=model_id,
            extraction_passes=extraction_passes,
            save_results=save_results
        )

        return JSONResponse(content={
            "status": "success",
            "filename": filename,
            "markdown_text": markdown_text,
            "total_entities": result["total_entities"],
            "entities": result["entities"]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LangExtract extraction failed: {str(e)}")


@app.post("/sentiment")
async def sentiment_endpoint(file: UploadFile = File(...)):
    """Analyze sentiment from PDF using FinBERT."""
    filename, markdown_text = await process_pdf(file)

    sentiments = analyze_sentiment(markdown_text)

    # Calculate aggregate sentiment
    if sentiments:
        avg_score = sum(s["score"] for s in sentiments) / len(sentiments)
        # Get most common label
        labels = [s["label"] for s in sentiments]
        dominant_label = max(set(labels), key=labels.count)
        aggregate = {"label": dominant_label, "avg_score": round(avg_score, 4)}
    else:
        aggregate = {"label": "neutral", "avg_score": 0.0}

    return JSONResponse(content={
        "status": "success",
        "filename": filename,
        "markdown_text": markdown_text,
        "total_sentences": len(sentiments),
        "sentiments": sentiments,
        "aggregate": aggregate
    })


@app.post("/analyze-all")
async def analyze_all_endpoint(
    file: UploadFile = File(...),
    model_id: str = Query(default="gemini-2.5-flash", description="Gemini model ID for LangExtract"),
    extraction_passes: int = Query(default=1, ge=1, le=3, description="Number of extraction passes")
):
    """Run all analyses (NER, LangExtract, Sentiment) on a PDF."""
    filename, markdown_text = await process_pdf(file)

    # NER
    ner_entities = extract_entities(markdown_text)
    ner_result = {
        "total_entities": len(ner_entities),
        "entities": ner_entities
    }

    # LangExtract
    try:
        langextract_result = extract_financial_info(
            text=markdown_text,
            model_id=model_id,
            extraction_passes=extraction_passes
        )
    except Exception as e:
        langextract_result = {"total_entities": 0, "entities": [], "error": str(e)}

    # Sentiment
    sentiments = analyze_sentiment(markdown_text)
    if sentiments:
        avg_score = sum(s["score"] for s in sentiments) / len(sentiments)
        labels = [s["label"] for s in sentiments]
        dominant_label = max(set(labels), key=labels.count)
        aggregate = {"label": dominant_label, "avg_score": round(avg_score, 4)}
    else:
        aggregate = {"label": "neutral", "avg_score": 0.0}
    sentiment_result = {
        "total_sentences": len(sentiments),
        "sentiments": sentiments,
        "aggregate": aggregate
    }

    return JSONResponse(content={
        "status": "success",
        "filename": filename,
        "markdown_text": markdown_text,
        "ner": ner_result,
        "langextract": langextract_result,
        "sentiment": sentiment_result
    })


@app.get("/")
async def root():
    return {
        "message": "NER Project API",
        "endpoints": {
            "convert_pdf": "/convert-pdf",
            "ner": "/ner",
            "langextract": "/langextract",
            "sentiment": "/sentiment",
            "analyze_all": "/analyze-all",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

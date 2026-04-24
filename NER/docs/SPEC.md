# NER Project - FastAPI Specification

## Overview

This project provides a FastAPI service with four main endpoints for processing financial documents:
1. **Document Conversion** - Convert PDF files to Markdown (existing)
2. **NER (Named Entity Recognition)** - Extract named entities using BERT
3. **LangExtract** - Extract financial entities using LangExtract + Gemini AI
4. **Sentiment Analysis** - Analyze sentiment using FinBERT

---

## API Endpoints

**All endpoints accept PDF file upload (`file` form field).**

---

### 1. POST `/convert-pdf`
Converts a PDF file to Markdown text. Pure utility endpoint when you only need the markdown.

**Request:**
- `file`: PDF file upload

**Response:**
```json
{
  "filename": "document.pdf",
  "status": "success",
  "markdown_text": "# Converted content..."
}
```

---

### 2. POST `/ner`
Extract named entities from PDF using BERT NER model.

**Request:**
- `file`: PDF file upload

**Response:**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "markdown_text": "# Converted markdown content...",
  "total_entities": 3,
  "entities": [
    {
      "entity_group": "ORG",
      "word": "Apple Inc.",
      "start": 0,
      "end": 10,
      "score": 0.99
    },
    {
      "entity_group": "PER",
      "word": "Tim Cook",
      "start": 42,
      "end": 50,
      "score": 0.98
    }
  ]
}
```

---

### 3. POST `/langextract`
Extract structured financial entities from PDF using LangExtract + Gemini AI.

**Request:**
- `file`: PDF file upload
- `model_id` (query, optional): Gemini model. Default: `gemini-2.5-flash`
- `extraction_passes` (query, optional): Number of passes (1-3). Default: 1
- `save_results` (query, optional): Save to JSONL. Default: false

**Response:**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "markdown_text": "# Converted markdown content...",
  "total_entities": 2,
  "entities": [
    {
      "class": "organization",
      "text": "Apple Inc.",
      "attributes": {"type": "technology company"}
    },
    {
      "class": "financial_metric",
      "text": "$117.9 billion",
      "attributes": {"metric_type": "quarterly revenue", "trend": "positive"}
    }
  ]
}
```

**Error Response (500):**
```json
{
  "detail": "LangExtract extraction failed: API key not found"
}
```

---

### 4. POST `/sentiment`
Analyze sentiment from PDF using FinBERT.

**Request:**
- `file`: PDF file upload

**Response:**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "markdown_text": "# Converted markdown content...",
  "total_sentences": 2,
  "sentiments": [
    {
      "sentence": "Apple Inc. reported strong quarterly earnings...",
      "label": "positive",
      "score": 0.93
    },
    {
      "sentence": "The company faced some challenges...",
      "label": "neutral",
      "score": 0.72
    }
  ],
  "aggregate": {
    "label": "positive",
    "avg_score": 0.85
  }
}
```

---

### 5. POST `/analyze-all`
Run all three analyses (NER, LangExtract, Sentiment) on a PDF in a single request.

**Request:**
- `file`: PDF file upload
- `model_id` (query, optional): Gemini model for LangExtract. Default: `gemini-2.5-flash`
- `extraction_passes` (query, optional): Number of passes. Default: 1

**Response:**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "markdown_text": "# Converted markdown content...",
  "ner": {
    "total_entities": 2,
    "entities": [...]
  },
  "langextract": {
    "total_entities": 3,
    "entities": [...]
  },
  "sentiment": {
    "total_sentences": 2,
    "sentiments": [...],
    "aggregate": {...}
  }
}
```

### 6. GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### 7. GET `/`
Root endpoint with API info.

**Response:**
```json
{
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
```

---

## File Structure

```
ner_project/
├── main.py              # FastAPI application (updated with new endpoints)
├── document_converter.py # PDF to Markdown conversion
├── ner_extractor.py     # BERT NER implementation
├── langextract_service.py # LangExtract financial extraction
├── sentiment_analysis.py  # FinBERT sentiment analysis
├── requirements.txt    # Dependencies (to be created)
└── SPEC.md             # This specification
```

---

## Implementation Notes

### PDF Processing Flow
1. User uploads PDF via `file` form field
2. Server saves to temp file
3. `document_converter.py` converts PDF → markdown
4. Markdown is returned in response AND passed to analysis functions
5. Temp file is deleted after processing

### Model Loading
- NER and Sentiment models are loaded at module import time
- LangExtract requires API key - returns error if not configured

### Error Handling
- All endpoints return appropriate HTTP status codes
- 400 Bad Request: Invalid input (non-PDF file)
- 404 Not Found: Resource not found
- 500 Internal Server Error: Processing failures (conversion, API errors)

### Common Response Fields
All analysis endpoints return:
- `status`: "success" or "error"
- `filename`: Original uploaded filename
- `markdown_text`: The converted markdown from the PDF
- Analysis-specific results

---

## Dependencies

```
fastapi
uvicorn
python-multipart
python-dotenv
torch
transformers
nltk
langextract
docling
```

---

## File Structure

```
ner_project/
├── main.py              # FastAPI application (updated with new endpoints)
├── document_converter.py # PDF to Markdown conversion
├── ner_extractor.py     # BERT NER implementation
├── langextract_service.py # LangExtract financial extraction
├── sentiment_analysis.py  # FinBERT sentiment analysis
├── requirements.txt    # Dependencies (to be created)
└── SPEC.md             # This specification
```

---

## Implementation Notes

### PDF Processing Flow
1. User uploads PDF file
2. `document_converter.py` converts PDF to Markdown
3. Analysis module processes the Markdown text
4. Both Markdown and analysis results returned

### Shared PDF Handling
- A helper function `process_pdf(file: UploadFile) -> tuple[str, str]` will:
  - Save uploaded PDF to temp file
  - Call `convert_document()` to get markdown
  - Clean up temp file
  - Returns `(filename, markdown_text)`

### Error Handling
- All endpoints return appropriate HTTP status codes
- 400 Bad Request: Invalid file type (not PDF)
- 404 Not Found: Resource not found
- 500 Internal Server Error: Processing failures (conversion, model inference)

### Performance Considerations
- Models are cached after first load
- LangExtract supports `max_workers` for parallel processing
- Consider adding async processing for large PDFs

---

## Dependencies

```
fastapi
uvicorn
python-multipart
python-dotenv
torch
transformers
nltk
langextract
docling
```

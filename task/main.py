from fastapi import FastAPI, UploadFile, File
import os

from document_converter import convert_pdf_to_markdown
from ner_extractor import extract_entities
from sentiment_analysis import analyze_sentiment

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Document Intelligence API Running 🚀"}


# 📄 PDF → Markdown
@app.post("/convert-pdf")
async def convert_pdf(file: UploadFile = File(...)):
    os.makedirs("converted_docs", exist_ok=True)

    file_path = os.path.join("converted_docs", file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    md_path = convert_pdf_to_markdown(file_path)

    return {
        "message": "PDF converted successfully",
        "markdown_file": md_path
    }


# 🧠 NER (FILE INPUT)
@app.post("/ner")
async def ner(file: UploadFile = File(...)):
    content = await file.read()

    try:
        text = content.decode("utf-8")
    except:
        return {"error": "Upload a valid .txt file"}

    return extract_entities(text)


# 😊 SENTIMENT (FILE INPUT)
@app.post("/sentiment")
async def sentiment(file: UploadFile = File(...)):
    content = await file.read()

    try:
        text = content.decode("utf-8")
    except:
        return {"error": "Upload a valid .txt file"}

    return analyze_sentiment(text)


# 🔥 COMBINED (BEST)
@app.post("/analyze-all")
async def analyze_all(file: UploadFile = File(...)):
    content = await file.read()

    try:
        text = content.decode("utf-8")
    except:
        return {"error": "Upload a valid .txt file"}

    return {
        "entities": extract_entities(text),
        "sentiment": analyze_sentiment(text)
    }
from fastapi import FastAPI, UploadFile, File
import os
from document_converter import convert_pdf_to_markdown

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Document Converter API",
        "endpoint": "/convert-pdf"
    }

@app.post("/convert-pdf")
async def convert_pdf(file: UploadFile = File(...)):

    file_path = os.path.join("converted_docs", file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    md_path = convert_pdf_to_markdown(file_path)

    return {
        "message": "PDF converted successfully",
        "markdown_file": md_path
    }

from fastapi import FastAPI, UploadFile, File
import fitz  # PyMuPDF
from markdownify import markdownify as md

app = FastAPI()

@app.get("/")
def home():
    return {"message": "PDF to Markdown API"}

@app.post("/convert-pdf-to-md/")
async def convert_pdf(file: UploadFile = File(...)):
    
    # Read uploaded pdf
    contents = await file.read()

    # Open PDF using PyMuPDF
    pdf = fitz.open(stream=contents, filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    # Convert text to markdown
    markdown_text = md(text)

    return {
        "markdown": markdown_text
    }
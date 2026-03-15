from fastapi import FastAPI, UploadFile, File
import os
from convert import pdf_to_markdown

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "PDF to Markdown API running"}


@app.post("/convert-pdf/")
async def convert_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # save uploaded pdf
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # convert pdf to markdown
    md_path = pdf_to_markdown(file_path)

    # read markdown content
    with open(md_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    return {
        "message": "Conversion successful",
        "markdown_file": md_path,
        "markdown_content": markdown_content
    }
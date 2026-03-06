import fitz  # PyMuPDF
from pathlib import Path


def convert_pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    output_path = Path(pdf_path).with_suffix(".txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return str(output_path)
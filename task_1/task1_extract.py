import os
import fitz  # PyMuPDF
import pdfplumber

PDF_DIR = "task1_pdfs"
OUTPUT_PYMUPDF = "outputs/pymupdf"
OUTPUT_PDFPLUMBER = "outputs/pdfplumber"


def extract_with_pymupdf(pdf_path):
    text = ""
    pdf = fitz.open(pdf_path)
    for page in pdf:
        text += page.get_text()
    return text


def extract_with_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


for pdf_file in os.listdir(PDF_DIR):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(PDF_DIR, pdf_file)

        # PyMuPDF output
        pymupdf_text = extract_with_pymupdf(pdf_path)
        with open(os.path.join(OUTPUT_PYMUPDF, pdf_file.replace(".pdf", ".txt")), "w", encoding="utf-8") as f:
            f.write(pymupdf_text)

        # pdfplumber output
        pdfplumber_text = extract_with_pdfplumber(pdf_path)
        with open(os.path.join(OUTPUT_PDFPLUMBER, pdf_file.replace(".pdf", ".txt")), "w", encoding="utf-8") as f:
            f.write(pdfplumber_text)

print("Text extraction completed for both parsers.")
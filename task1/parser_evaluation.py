import pdfplumber
import PyPDF2
import fitz 
import os
import re
from jiwer import wer

def clean_text(text):
    text = re.sub(r'[ ]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def extract_pdfplumber(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    return text

def extract_pypdf2(path):
    text = ""
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    return text

def extract_pymupdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text() + " "
    return text

if __name__ == "__main__":

    pdf_path = "test_documents/sample_report.pdf"

    print("\nExtracting text using different parsers...\n")

    text_pdfplumber = clean_text(extract_pdfplumber(pdf_path))
    text_pypdf2 = clean_text(extract_pypdf2(pdf_path))
    text_pymupdf = clean_text(extract_pymupdf(pdf_path))

    reference = text_pdfplumber  # baseline

    wer_pypdf2 = wer(reference, text_pypdf2)
    wer_pymupdf = wer(reference, text_pymupdf)

    print("Word Error Rate Results:")
    print(f"PyPDF2 WER  : {wer_pypdf2:.2%}")
    print(f"PyMuPDF WER : {wer_pymupdf:.2%}")

    os.makedirs("outputs", exist_ok=True)

    with open("outputs/pdfplumber.txt", "w", encoding="utf-8") as f:
        f.write(text_pdfplumber)

    with open("outputs/pypdf2.txt", "w", encoding="utf-8") as f:
        f.write(text_pypdf2)

    with open("outputs/pymupdf.txt", "w", encoding="utf-8") as f:
        f.write(text_pymupdf)

    print("\nExtraction completed. Cleaned texts saved in outputs folder.")

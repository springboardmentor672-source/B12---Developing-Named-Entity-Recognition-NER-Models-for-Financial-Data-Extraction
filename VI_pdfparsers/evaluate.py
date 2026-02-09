#                                       TASK 1

# Evaluated parsing libraries PyMuPDF, pdfplumber, and PyPDF2 using Word Error Rate (WER) 
# across two standardized PDF documents

import fitz  # PyMuPDF
import pdfplumber
from PyPDF2 import PdfReader
from jiwer import wer

# ----------- TEXT EXTRACTION FUNCTIONS -----------

def extract_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_pypdf2(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# ----------- WER EVALUATION -----------

import os

def evaluate(pdf_name):
    pdf_path = f"pdfs/{pdf_name}.pdf"
    gt_path = f"original/{pdf_name}.txt"

    # Read ground truth
    with open(gt_path, "r", encoding="utf-8") as f:
        reference_text = f.read()

    # Extract text
    pymupdf_text = extract_pymupdf(pdf_path)
    pdfplumber_text = extract_pdfplumber(pdf_path)
    pypdf2_text = extract_pypdf2(pdf_path)

    # Ensure outputs folder exists
    os.makedirs("outputs", exist_ok=True)

    # Save extracted outputs
    with open(f"outputs/{pdf_name}_pymupdf.txt", "w", encoding="utf-8") as f:
        f.write(pymupdf_text)

    with open(f"outputs/{pdf_name}_pdfplumber.txt", "w", encoding="utf-8") as f:
        f.write(pdfplumber_text)

    with open(f"outputs/{pdf_name}_pypdf2.txt", "w", encoding="utf-8") as f:
        f.write(pypdf2_text)

    # Calculate WER
    wer_pymupdf = wer(reference_text, pymupdf_text)
    wer_pdfplumber = wer(reference_text, pdfplumber_text)
    wer_pypdf2 = wer(reference_text, pypdf2_text)

    # Print results
    print(f"\n---Results for {pdf_name}.pdf---")
    print(f"PyMuPDF WER     : {wer_pymupdf}")
    print(f"pdfplumber WER : {wer_pdfplumber}")
    print(f"PyPDF2 WER     : {wer_pypdf2}")
    
    # ----------- RUN EVALUATION -----------

evaluate("pdf1")
evaluate("pdf2")


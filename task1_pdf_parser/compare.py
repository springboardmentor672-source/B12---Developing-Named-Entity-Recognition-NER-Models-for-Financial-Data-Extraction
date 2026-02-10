import pdfplumber
import fitz  # PyMuPDF
from jiwer import wer

print("Script started")

# Load ground truth text
with open("ground_truth/sample.txt", "r", encoding="utf-8") as f:
    ground_truth = f.read()

pdf_path = "pdf/sample.pdf"

def extract_pdfplumber(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_pymupdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

text1 = extract_pdfplumber(pdf_path)
text2 = extract_pymupdf(pdf_path)

print("WER (pdfplumber):", wer(ground_truth, text1))
print("WER (PyMuPDF):", wer(ground_truth, text2))

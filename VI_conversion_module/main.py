#                                        TASK 2

# Implemented a document conversion module that extracts text from PDF and DOCX files and 
# exports them into text format

import fitz  # PyMuPDF
from docx import Document
import os

# ---------- PDF to TXT ----------
def pdf_to_txt(pdf_path, output_txt):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)


# ---------- DOCX to TXT ----------
def docx_to_txt(docx_path, output_txt):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)


# ---------- MAIN ----------
input_folder = "input_files"
output_folder = "output_files"

for file in os.listdir(input_folder):
    input_path = os.path.join(input_folder, file)

    if file.endswith(".pdf"):
        output_path = os.path.join(output_folder, file.replace(".pdf", ".txt"))
        pdf_to_txt(input_path, output_path)
        print(f"Converted PDF: {file}")

    elif file.endswith(".docx"):
        output_path = os.path.join(output_folder, file.replace(".docx", ".txt"))
        docx_to_txt(input_path, output_path)
        print(f"Converted DOCX: {file}")


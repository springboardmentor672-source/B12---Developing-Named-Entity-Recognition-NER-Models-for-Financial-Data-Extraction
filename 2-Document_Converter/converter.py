import os
import fitz  # PyMuPDF
from docx import Document

# -------- PDF TEXT EXTRACTION USING PyMuPDF --------
def extract_text_from_pdf(pdf_path):
    text = ""
    pdf = fitz.open(pdf_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()
    return text


# -------- DOCX TEXT EXTRACTION --------
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# -------- SAVE OUTPUT --------
def save_text(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


# -------- MAIN LOGIC --------
input_folder = "input_files"
output_folder = "output_files"

for file in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file)

    if file.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
        output_name = file.replace(".pdf", ".txt")

    elif file.endswith(".docx"):
        text = extract_text_from_docx(file_path)
        output_name = file.replace(".docx", ".md")

    else:
        continue

    output_path = os.path.join(output_folder, output_name)
    save_text(text, output_path)

print("Document conversion completed successfully")
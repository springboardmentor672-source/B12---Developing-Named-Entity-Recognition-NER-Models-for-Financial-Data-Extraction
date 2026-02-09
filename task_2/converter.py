import os
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    lines = []
    for para in doc.paragraphs:
        lines.append(para.text)
    return "\n".join(lines)


def save_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def convert_document(input_file, output_format="txt"):
    name, ext = os.path.splitext(input_file)
    ext = ext.lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(input_file)
    elif ext == ".docx":
        text = extract_text_from_docx(input_file)
    else:
        raise ValueError("Unsupported file format")

    output_file = name + "." + output_format
    save_to_file(text, output_file)

    print("Conversion successful:", output_file)


if __name__ == "__main__":
    convert_document("input/sample.pdf", "txt")
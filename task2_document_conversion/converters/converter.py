import os
from converters.pdf_converter import extract_text_from_pdf
from converters.docx_converter import extract_text_from_docx

def convert_document(file_path, output_format="txt"):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        content = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        content = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

    return content

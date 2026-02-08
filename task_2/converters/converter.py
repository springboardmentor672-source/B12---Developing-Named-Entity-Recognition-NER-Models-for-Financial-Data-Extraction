from converters.pdf_converter import pdf_to_text
from converters.docx_converter import docx_to_text
import os

def convert_document(file_path):
    """
    Detect file type and extract text accordingly
    """
    if file_path.lower().endswith(".pdf"):
        return pdf_to_text(file_path)

    elif file_path.lower().endswith(".docx"):
        return docx_to_text(file_path)

    else:
        raise ValueError("Unsupported file format")


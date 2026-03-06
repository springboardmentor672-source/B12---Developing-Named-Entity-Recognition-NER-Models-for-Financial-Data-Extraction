import fitz  # PyMuPDF


def convert_pdf_to_text(pdf_path):
    """
    Extracts text from PDF file using PyMuPDF.
    """
    text = ""

    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"

    return text.strip()
import fitz  # PyMuPDF

def pdf_to_text(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF
    """
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return text


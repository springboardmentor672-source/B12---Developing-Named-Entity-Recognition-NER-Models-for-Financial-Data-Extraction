from docx import Document

def docx_to_text(docx_path):
    """
    Extract text from a DOCX file
    """
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


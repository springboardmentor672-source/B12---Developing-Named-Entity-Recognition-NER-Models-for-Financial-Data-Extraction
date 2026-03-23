from docling.document_converter import DocumentConverter
import os

def convert_pdf_to_markdown(file_path: str) -> str:
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    converter = DocumentConverter()
    result = converter.convert(file_path)

    markdown = result.document.export_to_markdown()

    return markdown
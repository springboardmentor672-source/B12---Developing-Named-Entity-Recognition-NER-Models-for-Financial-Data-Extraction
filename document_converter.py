from docling.document_converter import DocumentConverter
import os

converter = DocumentConverter()

def convert_pdf_to_markdown(file_path: str, output_dir: str = "converted_docs"):

    os.makedirs(output_dir, exist_ok=True)

    result = converter.convert(file_path)

    base_name = os.path.basename(file_path)
    md_path = os.path.join(output_dir, base_name + ".md")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(result.document.export_to_markdown())

    return md_path
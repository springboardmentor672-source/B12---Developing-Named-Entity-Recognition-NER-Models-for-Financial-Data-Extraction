from docling.document_converter import DocumentConverter

converter = DocumentConverter()

def convert_pdf_to_markdown(file_path: str) -> str:
    result = converter.convert(file_path)

    md_path = file_path + ".md"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(result.document.export_to_markdown())

    return md_path
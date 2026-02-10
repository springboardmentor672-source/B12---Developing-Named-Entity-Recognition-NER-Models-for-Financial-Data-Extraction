import os
import logging

# Kill OCR / RapidOCR spam
os.environ["LOGURU_LEVEL"] = "ERROR"
logging.getLogger().setLevel(logging.ERROR)

from docling.document_converter import DocumentConverter
from pathlib import Path

def convert_pdf_to_md(pdf_path, output_md_path):
    converter = DocumentConverter()

    result = converter.convert(pdf_path)
    markdown_content = result.document.export_to_markdown()

    output_md_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"✅ Conversion completed. Markdown saved at:\n{output_md_path.resolve()}")

if __name__ == "__main__":
    input_pdf = Path("td.pdf")
    output_md = Path("td.md")

    convert_pdf_to_md(input_pdf, output_md)

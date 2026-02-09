from docling.document_converter import DocumentConverter
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(BASE_DIR, "input_docs", "sample.pdf")
output_dir = os.path.join(BASE_DIR, "output_text")

os.makedirs(output_dir, exist_ok=True)

converter = DocumentConverter()
doc = converter.convert(input_file)

with open(os.path.join(output_dir, "docling.txt"), "w", encoding="utf-8") as f:
    f.write(doc.document.export_to_text())

print("Docling extraction completed")


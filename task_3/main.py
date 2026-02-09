from docling.document_converter import DocumentConverter
import json

SOURCE_FILE = "documents/apple.pdf"

converter = DocumentConverter()
result = converter.convert(SOURCE_FILE)

with open("apple.md", "w", encoding="utf-8") as f:
    f.write(result.document.export_to_markdown())

print("Successfully completed")

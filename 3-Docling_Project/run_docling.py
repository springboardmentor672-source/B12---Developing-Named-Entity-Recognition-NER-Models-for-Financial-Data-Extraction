from docling.document_converter import DocumentConverter

source = "input_files/sample.pdf"  # your document
converter = DocumentConverter()
result = converter.convert(source)
doc = result.document

# Save Markdown
with open("outputs/sample.md", "w", encoding="utf-8") as f:
    f.write(doc.export_to_markdown())


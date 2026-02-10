from docling.document_converter import DocumentConverter

converter = DocumentConverter()

result = converter.convert("input.pdf")

with open("output.md", "w", encoding="utf-8") as file:
    file.write(result.document.export_to_markdown())

print("PDF extracted successfully!")



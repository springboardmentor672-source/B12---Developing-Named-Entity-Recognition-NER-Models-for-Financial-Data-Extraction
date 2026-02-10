from docling.document_converter import DocumentConverter

# 1. Create converter
converter = DocumentConverter()

# 2. Convert PDF
result = converter.convert("sample.pdf")

# 3. Export as Markdown
markdown_text = result.document.export_to_markdown()

# 4. Save to .md file
with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown_text)

print("✅ PDF successfully converted to Markdown!")
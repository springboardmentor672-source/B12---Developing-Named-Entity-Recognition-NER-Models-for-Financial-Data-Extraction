from pathlib import Path
from docling.document_converter import DocumentConverter

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

pdfs = list(INPUT_DIR.glob("*.pdf"))
if not pdfs:
    print("No PDF files found in input directory.")
    exit()

converter = DocumentConverter()  # no arguments

for pdf_file in pdfs:
    result = converter.convert(pdf_file)

    output_path = OUTPUT_DIR / (pdf_file.stem + ".md")
    output_path.write_text(
        result.document.export_to_markdown(),
        encoding="utf-8"
    )

    print(f"Converted: {pdf_file.name} -> {output_path.name}")

import fitz  # PyMuPDF
from pathlib import Path

INPUT_DIR = "input"
OUTPUT_DIR = "output"

Path(OUTPUT_DIR).mkdir(exist_ok=True)

def convert_pdf_to_txt(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    output_file = Path(OUTPUT_DIR) / (Path(pdf_path).stem + ".txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Converted: {pdf_path.name} → {output_file.name}")

for pdf_file in Path(INPUT_DIR).glob("*.pdf"):
    convert_pdf_to_txt(pdf_file)



import fitz  # PyMuPDF

pdf_file = "infosys-ar-25.pdf"

output_txt = "input.txt"

doc = fitz.open(pdf_file)

with open(output_txt, "w", encoding="utf-8") as f:
    for page in doc:
        text = page.get_text()
        f.write(text)

print("Text extracted and saved as input.txt")
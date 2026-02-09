import fitz  # PyMuPDF

doc = fitz.open("../pdfs/sample.pdf")
text = ""

for page in doc:
    text += page.get_text()

with open("../outputs/pymupdf.txt", "w", encoding="utf-8") as f:
    f.write(text)
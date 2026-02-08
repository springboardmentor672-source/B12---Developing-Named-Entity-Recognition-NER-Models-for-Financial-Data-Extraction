import fitz

doc = fitz.open("sample.pdf")
text = ""

for page in doc:
    text += page.get_text()

with open("pymupdf.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("PyMuPDF extraction completed")



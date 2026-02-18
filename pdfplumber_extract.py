import pdfplumber

text = ""

with pdfplumber.open("sample.pdf") as pdf:
    for page in pdf.pages:
        text += page.extract_text() or ""

open("pdfplumber_output.txt", "w", encoding="utf-8").write(text)

print("pdfplumber extraction done")

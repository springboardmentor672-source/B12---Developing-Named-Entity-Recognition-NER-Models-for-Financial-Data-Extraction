import pdfplumber

text = ""

with pdfplumber.open("../pdfs/sample.pdf") as pdf:
    for page in pdf.pages:
        text += page.extract_text()

with open("../outputs/pdfplumber.txt", "w", encoding="utf-8") as f:
    f.write(text)
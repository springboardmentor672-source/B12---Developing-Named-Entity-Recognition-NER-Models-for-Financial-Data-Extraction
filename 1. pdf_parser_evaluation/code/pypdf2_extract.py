from PyPDF2 import PdfReader

reader = PdfReader("../pdfs/sample.pdf")
text = ""

for page in reader.pages:
    text += page.extract_text()

with open("../outputs/pypdf2.txt", "w", encoding="utf-8") as f:
    f.write(text)
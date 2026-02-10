import fitz

doc = fitz.open("sample.pdf")
text = ""

for page in doc:
    text += page.get_text()

open("sample.txt", "w", encoding="utf-8").write(text)

print("Converted to sample.txt")

from pdfminer.high_level import extract_text

text = extract_text("sample.pdf")

with open("pdfminer.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("PDFMiner extraction completed")


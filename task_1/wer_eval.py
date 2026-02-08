from jiwer import wer

with open("pymupdf.txt", "r", encoding="utf-8") as f:
    reference = f.read()

with open("pdfminer.txt", "r", encoding="utf-8") as f:
    hypothesis = f.read()

wer_score = wer(reference, hypothesis)

print("WER (PDFMiner vs PyMuPDF):", wer_score)


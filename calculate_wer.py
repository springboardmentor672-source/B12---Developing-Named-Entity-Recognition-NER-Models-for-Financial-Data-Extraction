

from jiwer import wer

with open("groundtruth.txt", encoding="utf-8") as f:
    ref = f.read()
with open("pymupdf_output.txt", encoding="utf-8") as f:
    pymu = f.read()
with open("pdfplumber_output.txt", encoding="utf-8") as f:
    plum = f.read()

print("PyMuPDF WER:", wer(ref, pymu))
print("pdfplumber WER:", wer(ref, plum))

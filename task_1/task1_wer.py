import os
from jiwer import wer

GROUND_TRUTH_DIR = "ground_truth"
PYMUPDF_DIR = "outputs/pymupdf"
PDFPLUMBER_DIR = "outputs/pdfplumber"

def read_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

results = []

for file_name in os.listdir(GROUND_TRUTH_DIR):
    if file_name.endswith(".txt"):
        gt_text = read_text(os.path.join(GROUND_TRUTH_DIR, file_name))

        pymupdf_text = read_text(os.path.join(PYMUPDF_DIR, file_name))
        pdfplumber_text = read_text(os.path.join(PDFPLUMBER_DIR, file_name))

        wer_pymupdf = wer(gt_text, pymupdf_text)
        wer_pdfplumber = wer(gt_text, pdfplumber_text)

        results.append((file_name, wer_pymupdf, wer_pdfplumber))

print("WER Results:\n")
for file_name, w1, w2 in results:
    print(f"{file_name}")
    print(f"  PyMuPDF WER     : {w1:.3f}")
    print(f"  pdfplumber WER : {w2:.3f}\n")
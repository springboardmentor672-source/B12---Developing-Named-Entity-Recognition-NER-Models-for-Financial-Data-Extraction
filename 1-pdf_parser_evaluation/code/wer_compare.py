from jiwer import wer

def calculate_wer(ref, hyp):
    with open(ref, "r", encoding="utf-8") as f:
        reference = f.read()
    with open(hyp, "r", encoding="utf-8") as f:
        hypothesis = f.read()
    return wer(reference, hypothesis)

print("PyPDF2 WER:", calculate_wer("../ground_truth/sample.txt", "../outputs/pypdf2.txt"))
print("pdfplumber WER:", calculate_wer("../ground_truth/sample.txt", "../outputs/pdfplumber.txt"))
print("PyMuPDF WER:", calculate_wer("../ground_truth/sample.txt", "../outputs/pymupdf.txt"))
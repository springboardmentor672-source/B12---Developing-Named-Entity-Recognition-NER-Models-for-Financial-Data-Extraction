from jiwer import wer

with open("my_output_pymupdf_clean.txt", "r", encoding="utf-8") as f:
    ref_clean = f.read()

with open("my_output_pdfminer_clean.txt", "r", encoding="utf-8") as f:
    hyp_clean = f.read()

final_score = wer(ref_clean, hyp_clean)

print(f"Original WER: 0.339")
print(f"Cleaned WER:  {final_score}")
from jiwer import wer
import os

# 1. Load the text from the first extraction (Reference)
with open("my_output_pymupdf.txt", "r", encoding="utf-8") as f:
    reference = f.read()

# 2. Load the text from the second extraction (Hypothesis)
with open("my_output_pdfminer.txt", "r", encoding="utf-8") as f:
    hypothesis = f.read()

# 3. Calculate the Word Error Rate
# This tells us the percentage of words that differ
error_score = wer(reference, hypothesis)

print("-" * 30)
print(f"WER Score: {error_score}")
print("-" * 30)

if error_score == 0:
    print("The files are identical!")
elif error_score < 0.1:
    print("The files are very similar (less than 10% difference).")
else:
    print(f"Significant differences detected ({error_score * 100:.2f}%).")
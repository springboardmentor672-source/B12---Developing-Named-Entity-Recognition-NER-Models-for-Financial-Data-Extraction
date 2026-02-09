# -- To use a docling parser to parse a pdf and 
# to calculate the WER value of the parser --

# -------- Importing required libraries --------
from docling.document_converter import DocumentConverter
from jiwer import wer
import os

# -------- File paths --------
pdf_path = "input_files/Financial results of tata.pdf"
reference_text_path = "reference_text/fin_res.txt"
output_markdown_path = "output_files/docling_output.md"

# -------- Using Docling to extract text --------
converter = DocumentConverter()
result = converter.convert(pdf_path)

# -------- Converting extracted document to MARKDOWN --------
extracted_markdown = result.document.export_to_markdown()

# -------- Saving extracted markdown to file --------
with open(output_markdown_path, "w", encoding="utf-8") as f:
    f.write(extracted_markdown)

print(">>> Extracted markdown saved to output_files/docling_output.md")

# -------- Reading reference text --------
with open(reference_text_path, "r", encoding="utf-8") as f:
    reference_text = f.read()

# -------- Calculating WER --------
wer_score = wer(reference_text, extracted_markdown)

print(">>> Word Error Rate (WER):", wer_score)
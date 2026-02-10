import fitz  # PyMuPDF
import pdfplumber
import difflib
from pathlib import Path


def extract_pymupdf(file_path):
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(file_path)
    text = []
    for page in doc:
        page_text = page.get_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)


def extract_pdfplumber(file_path):
    """Extract text from PDF using pdfplumber."""
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def compare_texts(text1, text2):
    """Return a unified diff of two texts."""
    return "\n".join(
        difflib.unified_diff(
            text1.splitlines(),
            text2.splitlines(),
            fromfile="PyMuPDF",
            tofile="pdfplumber",
            lineterm=""
        )
    )


def main():
    pdf_path = Path("sample.pdf")
    output_path = Path("doc.txt")

    if not pdf_path.exists():
        raise FileNotFoundError("sample.pdf not found")

    print("Extracting text with PyMuPDF...")
    pymupdf_text = extract_pymupdf(pdf_path)

    print("Extracting text with pdfplumber...")
    pdfplumber_text = extract_pdfplumber(pdf_path)

    diff = compare_texts(pymupdf_text, pdfplumber_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== PyMuPDF OUTPUT ===\n")
        f.write(pymupdf_text)
        f.write("\n\n=== pdfplumber OUTPUT ===\n")
        f.write(pdfplumber_text)
        f.write("\n\n=== DIFF (PyMuPDF vs pdfplumber) ===\n")
        f.write(diff if diff else "No differences found.")

    print(f"Comparison written to {output_path.resolve()}")


if __name__ == "__main__":
    main()


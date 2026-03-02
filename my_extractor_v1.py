import fitz
import os
import sys

# 1. Print current working directory so we know WHERE Python is looking
print(f"Current Folder: {os.getcwd()}")

pdf_path = "sample.pdf"

if not os.path.exists(pdf_path):
    print(f"FAILED: I cannot see {pdf_path} in the current folder.")
    # List all files in the folder to see what IS there
    print(f"Files I can see: {os.listdir('.')}")
else:
    print(f"FOUND: {pdf_path} is present. Attempting to open...")
    try:
        doc = fitz.open(pdf_path)
        print(f"SUCCESS: Opened PDF. Total pages: {len(doc)}")
        
        full_text = ""
        for i, page in enumerate(doc):
            full_text += page.get_text()
            if i == 0:
                print("DEBUG: Successfully extracted text from Page 1.")
            
        with open("my_output_pymupdf.txt", "w", encoding="utf-8") as f:
            f.write(full_text)
            
        print("--- FINAL CHECK ---")
        if os.path.exists("my_output_pymupdf.txt"):
            print(f"COMPLETE: 'my_output_pymupdf.txt' was created! Size: {os.path.getsize('my_output_pymupdf.txt')} bytes")
        else:
            print("ERROR: Script finished but the output file is missing!")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
import os
import sys

try:
    from pdfminer.high_level import extract_text
    print("DEBUG: Library 'pdfminer' loaded successfully.")
except ImportError:
    print("DEBUG: Library 'pdfminer' NOT FOUND. Run 'pip install pdfminer.six'")
    sys.exit()

pdf_path = "sample.pdf"
output_path = "my_output_pdfminer.txt"

print(f"DEBUG: Checking for {pdf_path}...")
if os.path.exists(pdf_path):
    print(f"DEBUG: Found {pdf_path}. Starting extraction (this is slow)...")
    try:
        # This is the line where it usually hangs or fails
        text = extract_text(pdf_path)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        print(f"SUCCESS: {output_path} created! Size: {os.path.getsize(output_path)} bytes.")
    except Exception as e:
        print(f"EXTRACTION ERROR: {e}")
else:
    print(f"FAILED: Cannot find {pdf_path} in {os.getcwd()}")
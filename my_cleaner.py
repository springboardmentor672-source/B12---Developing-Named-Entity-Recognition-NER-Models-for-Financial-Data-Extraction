import os
import re

def clean_text(text):
    # 1. Convert to lowercase (Standardizes everything)
    text = text.lower()
    
    # 2. Remove special characters like \f (Form Feed) and \n (Newlines)
    # We replace them with a space so words don't stick together
    text = re.sub(r'[\n\f\t]', ' ', text)
    
    # 3. Remove non-alphanumeric characters (keep only letters and numbers)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # 4. Remove extra whitespaces (Changes "hello    world" to "hello world")
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# --- Processing the files ---

files_to_clean = ["my_output_pymupdf.txt", "my_output_pdfminer.txt"]

for filename in files_to_clean:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            raw_data = f.read()
        
        cleaned_data = clean_text(raw_data)
        
        # Save as a new "clean" version
        new_filename = filename.replace(".txt", "_clean.txt")
        with open(new_filename, "w", encoding="utf-8") as f:
            f.write(cleaned_data)
            
        print(f"Cleaned: {new_filename}")
import os
import sys

# Import the tools you built
from converter import DocumentConverter
from nlp_processor import PurePythonNLP

def main():
    print("==========================================")
    print("   FINANCIAL DOCUMENT PARSER PIPELINE     ")
    print("==========================================")

    # 1. Setup paths
    pdf_folder = "./data/pdfs"
    output_folder = "./output"
    
    # 2. Get user input
    filename = input("\nEnter the PDF filename (e.g., earnings.pdf): ").strip()
    input_path = os.path.join(pdf_folder, filename)
    
    # 3. Check file
    if not os.path.exists(input_path):
        print(f"❌ Error: File '{filename}' not found in {pdf_folder}")
        return

    # --- STAGE 1: CONVERSION ---
    print(f"\n[Stage 1] Converting {filename}...")
    converter = DocumentConverter()
    
    # We convert to 'txt' so the NLP processor can read it
    result_msg = converter.convert(input_path, output_format='txt')
    print(result_msg)
    
    # Define where the text file landed
    text_filename = os.path.splitext(filename)[0] + ".txt"
    text_path = os.path.join(output_folder, text_filename)

    # --- STAGE 2: NLP ANALYSIS ---
    print(f"\n[Stage 2] Running NLP Analysis...")
    
    # Read the fresh text file
    with open(text_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    nlp = PurePythonNLP()
    
    # Clean & Tokenize
    cleaned_text = nlp.clean_text(raw_text)
    tokens = nlp.tokenize(cleaned_text)
    filtered = nlp.remove_stopwords(tokens)
    
    print(f"   > Original size: {len(raw_text)} chars")
    print(f"   > Cleaned size:  {len(cleaned_text)} chars")
    print(f"   > Tokens found:  {len(filtered)} (financial terms preserved!)")

    # --- STAGE 3: REPORT ---
    print("\n[Stage 3] Generating Sample Analysis...")
    comparison = nlp.run_comparison(filtered)
    
    # Show a snippet of the analysis
    print("-" * 60)
    print(f"{'ORIGINAL':<15} | {'STEMMED':<15} | {'LEMMATIZED':<15}")
    print("-" * 60)
    
    # Show first 10 relevant words
    for orig, stem, lemma in comparison[20:30]:
        print(f"{orig:<15} | {stem:<15} | {lemma:<15}")
    print("-" * 60)
    
    print("\n✅ PIPELINE COMPLETE.")

if __name__ == "__main__":
    main()
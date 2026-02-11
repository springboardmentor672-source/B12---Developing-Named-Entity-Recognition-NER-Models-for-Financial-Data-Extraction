import os
import sys

# --- IMPORTS ---
from converter import DocumentConverter
from nlp_processor import PurePythonNLP
from financial_ner import FinancialNER, save_to_markdown  # New Import!

# --- CONFIGURATION ---
# PASTE YOUR HUGGING FACE TOKEN HERE
HF_TOKEN = "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" 

def main():
    print("==================================================")
    print("      FINANCIAL DOCUMENT PARSER PIPELINE          ")
    print("      (Conversion -> NLP -> NER Analysis)         ")
    print("==================================================")

    # 1. Setup paths
    pdf_folder = "./data/pdfs"
    output_folder = "./output"
    
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 2. Get user input
    filename = input("\nEnter the PDF filename (e.g., earnings.pdf): ").strip()
    input_path = os.path.join(pdf_folder, filename)
    
    # 3. Check file
    if not os.path.exists(input_path):
        print(f"❌ Error: File '{filename}' not found in {pdf_folder}")
        return

    # ---------------------------------------------------------
    # STAGE 1: DOCUMENT CONVERSION
    # ---------------------------------------------------------
    print(f"\n[Stage 1] Converting PDF to Text...")
    converter = DocumentConverter()
    
    # Convert PDF -> TXT
    result_msg = converter.convert(input_path, output_format='txt')
    print(f"   > {result_msg}")
    
    # Define the text file path
    text_filename = os.path.splitext(filename)[0] + ".txt"
    text_path = os.path.join(output_folder, text_filename)

    # ---------------------------------------------------------
    # STAGE 2: NLP PRE-PROCESSING
    # ---------------------------------------------------------
    print(f"\n[Stage 2] Running NLP Cleaning & Tokenization...")
    
    # Read the text file
    with open(text_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    nlp = PurePythonNLP()
    
    # Clean & Tokenize
    cleaned_text = nlp.clean_text(raw_text)
    tokens = nlp.tokenize(cleaned_text)
    filtered = nlp.remove_stopwords(tokens)
    
    print(f"   > Original size: {len(raw_text)} chars")
    print(f"   > Cleaned size:  {len(cleaned_text)} chars")
    print(f"   > Tokens found:  {len(filtered)} (stopwords removed)")

    # ---------------------------------------------------------
    # STAGE 3: NLP ANALYSIS REPORT
    # ---------------------------------------------------------
    print("\n[Stage 3] Generating Linguistic Report...")
    comparison = nlp.run_comparison(filtered)
    
    # Show a snippet (words 20-30)
    print("-" * 60)
    print(f"{'ORIGINAL':<15} | {'STEMMED':<15} | {'LEMMATIZED':<15}")
    print("-" * 60)
    for orig, stem, lemma in comparison[20:30]:
        print(f"{orig:<15} | {stem:<15} | {lemma:<15}")
    print("-" * 60)

    # ---------------------------------------------------------
    # STAGE 4: FINANCIAL ENTITY RECOGNITION (NER)
    # ---------------------------------------------------------
    print("\n[Stage 4] Running Financial NER Analysis...")
    
    if not HF_TOKEN or "hf_" not in HF_TOKEN:
        print("   ❌ Error: Hugging Face Token is missing or invalid.")
        print("   Please update 'HF_TOKEN' at the top of main.py")
    else:
        # Initialize the Financial NER Engine
        ner_engine = FinancialNER(HF_TOKEN)
        
        # Run analysis on the raw (but text-extracted) content
        # We use raw_text because NER needs context (sentences), not just list of tokens
        ner_results = ner_engine.analyze(raw_text)
        
        # Define report path
        report_filename = os.path.splitext(filename)[0] + "_financial_report.md"
        report_path = os.path.join(output_folder, report_filename)
        
        # Save to Markdown
        save_to_markdown(ner_results, report_path)
        
        print(f"\n   ✅ FINANCIAL REPORT GENERATED: {report_path}")

    print("\n==================================================")
    print("           PIPELINE COMPLETE SUCCESS              ")
    print("==================================================")

if __name__ == "__main__":
    main()
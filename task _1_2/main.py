import os
import sys

# --- IMPORTS ---
from converter import DocumentConverter
from nlp_processor import PurePythonNLP
from financial_ner import FinancialNER, save_to_markdown
from sentiment_module import FinancialSentiment  # <--- NEW IMPORT

# --- CONFIGURATION ---
# PASTE YOUR WORKING TOKEN HERE
HF_TOKEN = "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" 

def main():
    print("==================================================")
    print("      FINANCIAL DOCUMENT PARSER PIPELINE          ")
    print("      (Conversion -> NLP -> NER -> Sentiment)     ")
    print("==================================================")

    # 1. Setup paths
    pdf_folder = "./data/pdfs"
    output_folder = "./output"
    
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
    result_msg = converter.convert(input_path, output_format='txt')
    print(f"   > {result_msg}")
    
    text_filename = os.path.splitext(filename)[0] + ".txt"
    text_path = os.path.join(output_folder, text_filename)

    # ---------------------------------------------------------
    # STAGE 2: NLP PRE-PROCESSING
    # ---------------------------------------------------------
    print(f"\n[Stage 2] Running NLP Cleaning...")
    with open(text_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    nlp = PurePythonNLP()
    cleaned_text = nlp.clean_text(raw_text)
    
    print(f"   > Text cleaned successfully ({len(cleaned_text)} chars).")

    # ---------------------------------------------------------
    # STAGE 3: FINANCIAL ENTITY RECOGNITION (NER)
    # ---------------------------------------------------------
    print("\n[Stage 3] Extracting Financial Entities...")
    
    if not HF_TOKEN or "hf_" not in HF_TOKEN:
        print("   ❌ Error: Token missing. Please update HF_TOKEN in main.py")
        return

    ner_engine = FinancialNER(HF_TOKEN)
    ner_results = ner_engine.analyze(raw_text)
    
    ner_report_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_entities.md")
    save_to_markdown(ner_results, ner_report_path)
    print(f"   ✅ Entity Report saved.")

    # ---------------------------------------------------------
    # STAGE 4: SENTIMENT ANALYSIS (NEW)
    # ---------------------------------------------------------
    print("\n[Stage 4] Analyzing Financial Sentiment...")
    
    sentiment_engine = FinancialSentiment(HF_TOKEN)
    sentiment_results = sentiment_engine.analyze(raw_text)
    
    sent_report_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_sentiment.md")
    sentiment_engine.save_report(sentiment_results, sent_report_path)
    print(f"   ✅ Sentiment Report saved.")

    print("\n==================================================")
    print("           PIPELINE COMPLETE SUCCESS              ")
    print("==================================================")

if __name__ == "__main__":
    main()
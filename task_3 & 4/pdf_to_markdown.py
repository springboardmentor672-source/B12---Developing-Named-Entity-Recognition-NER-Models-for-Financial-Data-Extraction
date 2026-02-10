import pdfplumber
import os

def convert_to_markdown(pdf_path, md_path):
    print(f"📄 Processing: {pdf_path}...")
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found at {pdf_path}")
        return

    markdown_content = f"# Extracted Content from {os.path.basename(pdf_path)}\n\n"
    
    try:
        # Use the tool we KNOW works (pdfplumber)
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                # Extract text
                text = page.extract_text()
                
                if text:
                    # Add a nice Markdown Header for each page
                    markdown_content += f"## Page {i + 1}\n\n"
                    markdown_content += text + "\n\n"
                    markdown_content += "---\n\n" # Horizontal rule divider

        # Save to .md file
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        print(f"✅ Success! Markdown file saved to: {md_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Define paths
    input_file = "./data/pdfs/earnings.pdf"
    output_file = "./output/earnings.md"
    
    # Run conversion
    convert_to_markdown(input_file, output_file)
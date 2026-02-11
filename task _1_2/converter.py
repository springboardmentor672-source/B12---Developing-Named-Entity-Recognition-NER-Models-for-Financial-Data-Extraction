import os
import pdfplumber
from docx import Document

class DocumentConverter:
    def convert(self, input_path, output_format='txt'):
        """Detects file type and converts it."""
        if not os.path.exists(input_path):
            return f"❌ Error: File not found at {input_path}"

        print(f"📄 Processing: {os.path.basename(input_path)}...")
        
        ext = os.path.splitext(input_path)[1].lower()
        if ext == '.pdf':
            content = self._pdf_to_text(input_path)
        elif ext == '.docx':
            content = self._docx_to_text(input_path)
        else:
            return f"❌ Error: Unsupported file type '{ext}'"

        return self._save_output(input_path, content, output_format)

    def _pdf_to_text(self, path):
        text = ""
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {e}"

    def _docx_to_text(self, path):
        text = ""
        try:
            doc = Document(path)
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {e}"

    def _save_output(self, input_path, content, output_format):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.basename(input_path)
        file_name = os.path.splitext(base_name)[0] + "." + output_format
        output_path = os.path.join(output_dir, file_name)

        # Add a simple Markdown header if requested
        if output_format == 'md':
            header = f"# Extracted Content from {base_name}\n---\n\n"
            content = header + content

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"✅ Success! Saved to: {output_path}"

if __name__ == "__main__":
    converter = DocumentConverter()
    
    # Interactive Mode
    pdf_dir = "./data/pdfs"
    print("\n--- Document Converter ---")
    
    target = input("Enter filename (e.g. earnings.pdf): ")
    format_choice = input("Output format (txt or md)? [default: txt]: ").lower() or 'txt'
    
    full_path = os.path.join(pdf_dir, target)
    print(converter.convert(full_path, output_format=format_choice))
from docling.document_converter import DocumentConverter
import os

def convert_document(file_path: str, output_dir: str = None) -> str:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    converter = DocumentConverter()
    
    result = converter.convert(file_path)
    
    text = result.document.export_to_markdown()
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    return text

from docling.document_converter import DocumentConverter
import os

def convert_document(file_path: str, output_dir: str = None) -> str:
    converter = DocumentConverter()

    result = converter.convert(file_path)

    text = result.document.export_to_markdown()

    # Save file if output_dir provided
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.md")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

    return text
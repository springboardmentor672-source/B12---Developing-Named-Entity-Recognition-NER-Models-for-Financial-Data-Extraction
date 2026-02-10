import fitz 
import docx
import os
import argparse



def extract_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_data = []

    for page in doc:
        text_data.append(page.get_text())

    doc.close()
    return "\n".join(text_data)



def extract_from_docx(docx_path):
    document = docx.Document(docx_path)
    text_data = []

    for para in document.paragraphs:
        if para.text.strip():
            text_data.append(para.text.strip())

    return "\n".join(text_data)



def save_text(text, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)



def convert_file(input_file, output_format):
    filename = os.path.basename(input_file)
    name = os.path.splitext(filename)[0]

    if input_file.lower().endswith(".pdf"):
        text = extract_from_pdf(input_file)

    elif input_file.lower().endswith(".docx"):
        text = extract_from_docx(input_file)

    else:
        raise ValueError("Only PDF and DOCX are supported")

    output_file = f"{name}.{output_format}"
    save_text(text, output_file)
    print(f"✅ File saved as: {output_file}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF/DOCX to TXT/MD Converter")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--format", choices=["txt", "md"], default="txt")

    args = parser.parse_args()

    convert_file(args.input, args.format)

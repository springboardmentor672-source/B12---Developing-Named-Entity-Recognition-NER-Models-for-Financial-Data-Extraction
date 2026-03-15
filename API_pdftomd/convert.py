import fitz
import os

def pdf_to_markdown(pdf_path, output_folder="outputs"):

    # create output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    # open pdf
    doc = fitz.open(pdf_path)

    markdown_text = ""

    # extract text from each page
    for page in doc:
        text = page.get_text()
        markdown_text += text + "\n\n"

    # create markdown file name
    filename = os.path.basename(pdf_path).replace(".pdf", ".md")
    md_path = os.path.join(output_folder, filename)

    # save markdown file
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)

    return md_path
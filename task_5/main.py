from pdf_processor import convert_pdf_to_text
from ner_module import combined_financial_ner


def main():
    pdf_path = "input/tdm.pdf"

    print("Extracting text from PDF...")
    text_file = convert_pdf_to_text(pdf_path)

    with open(text_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    print("Running Financial + General NER...")
    results = combined_financial_ner(text_content)

    print("\n========== FINANCIAL ENTITIES ==========")
    for entity in results["financial_entities"]:
        print(entity)

    print("\n========== GENERAL ENTITIES ==========")
    for entity in results["general_entities"]:
        print(entity)


if __name__ == "__main__":
    main()
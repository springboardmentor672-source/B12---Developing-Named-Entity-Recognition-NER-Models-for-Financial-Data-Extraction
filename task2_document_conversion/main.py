import os
from converters.converter import convert_document

def main():
    input_folder = "input_docs"
    output_folder = "output_text"

    os.makedirs(output_folder, exist_ok=True)

    try:
        files = os.listdir(input_folder)

        if not files:
            raise FileNotFoundError("No documents found in input_docs folder")

        for file in files:
            # 🔒 Ignore temp/hidden files
            if file.startswith("~$"):
                continue

            # 🔒 Process only PDF and DOCX
            if not file.lower().endswith((".pdf", ".docx")):
                continue

            input_path = os.path.join(input_folder, file)

            print(f"Processing: {file}")
            convert_document(input_path, output_folder)

        print("\n✅ Document conversion completed successfully")

    except FileNotFoundError as e:
        print(f"❌ File error: {e}")

    except ValueError as e:
        print(f"❌ Format error: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()

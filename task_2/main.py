from converters.converter import convert_document
import os

# Change this to test PDF or DOCX
input_file = "input_docs/sample.pdf"
# input_file = "input_docs/sample.docx"

# Extract text
text = convert_document(input_file)

# Output file name (without extension)
base_name = os.path.splitext(os.path.basename(input_file))[0]

# Save as .txt
with open(f"output_text/{base_name}.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Save as .md
with open(f"output_text/{base_name}.md", "w", encoding="utf-8") as f:
    f.write(text)

print("Document conversion completed successfully")


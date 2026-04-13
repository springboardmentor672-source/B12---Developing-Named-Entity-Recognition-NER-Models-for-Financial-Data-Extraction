from transformers import AutoTokenizer, AutoModelForTokenClassification

model_name = "dslim/bert-base-NER"

print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Downloading model...")
model = AutoModelForTokenClassification.from_pretrained(model_name)

print("Download complete ✅")
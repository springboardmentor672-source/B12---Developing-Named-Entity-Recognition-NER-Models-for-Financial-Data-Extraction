# Task 3: Text Cleaning, Tokenization, Stopword Removal,
# Stemming vs Lemmatization (using Task 2 output)

import re
from pathlib import Path
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# download stopwords (runs once)
nltk.download("stopwords")

# load NLP tools
nlp = spacy.load("en_core_web_sm")
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

# --------------------------------------------------
# STEP 1: READ TEXT FROM TASK 2 OUTPUT
# --------------------------------------------------
input_file = Path("../task2_document_converter/output/sample.md")

text = input_file.read_text(encoding="utf-8")

# --------------------------------------------------
# STEP 2: TEXT CLEANING
# --------------------------------------------------
def clean_text(text):
    text = re.sub(r"\n+", " ", text)       # remove newlines
    text = re.sub(r"\s+", " ", text)       # remove extra spaces
    text = re.sub(r"\b\d+\b", "", text)    # remove page numbers
    return text.lower().strip()

cleaned_text = clean_text(text)

# --------------------------------------------------
# STEP 3: TOKENIZATION (keep $, %, /)
# --------------------------------------------------
def tokenize(text):
    return re.findall(r"\$?\d+%?|\w+\/\w+|\w+", text)

tokens = tokenize(cleaned_text)

# --------------------------------------------------
# STEP 4: STOP WORD REMOVAL
# --------------------------------------------------
filtered_tokens = [t for t in tokens if t not in stop_words]

# --------------------------------------------------
# STEP 5: STEMMING
# --------------------------------------------------
stemmed_tokens = [stemmer.stem(t) for t in filtered_tokens]

# --------------------------------------------------
# STEP 6: LEMMATIZATION
# --------------------------------------------------
doc = nlp(" ".join(filtered_tokens))
lemmatized_tokens = [token.lemma_ for token in doc]

# --------------------------------------------------
# STEP 7: OUTPUT RESULTS
# --------------------------------------------------
print("\n--- CLEANED TOKENS ---")
print(filtered_tokens[:30])

print("\n--- STEMMING OUTPUT ---")
print(stemmed_tokens[:30])

print("\n--- LEMMATIZATION OUTPUT ---")
print(lemmatized_tokens[:30])
